import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
from styles import CSS, JS, EXAMPLES, HEADER_HTML
from database import init_db, save_research, get_all_research

load_dotenv(override=True)
init_db()


def _trunc(text: str, limit: int = 50) -> str:
    return text[:limit] + "..." if len(text) > limit else text


def load_catalog():
    rows = get_all_research()
    data, records = [], []
    for r in rows:
        data.append([r["id"], r["created_at"], _trunc(r["user_query"]), _trunc(r["research_output"])])
        records.append({"query": r["user_query"], "output": r["research_output"]})
    return data, records


async def run(query: str):
    final_report = None
    async for status_update in ResearchManager().run(query):
        final_report = status_update
        yield status_update, gr.update(), gr.update()
    if final_report:
        save_research(query, final_report)
    data, records = load_catalog()
    yield final_report, data, records


with gr.Blocks(title="Deep Research") as ui:
    gr.HTML(HEADER_HTML)

    with gr.Row(elem_classes="dr-query-row"):
        query_textbox = gr.Textbox(
            placeholder="Type a research question...",
            show_label=False,
            container=False,
            autofocus=True,
            elem_id="dr-query",
            scale=5,
        )
        run_button = gr.Button("Investigate", variant="primary", elem_id="dr-run", scale=1)

    gr.HTML('<div class="dr-examples-label">Try one</div>')
    gr.Examples(examples=EXAMPLES, inputs=query_textbox, elem_id="dr-examples")

    report = gr.Markdown(elem_id="dr-report")

    # Research Catalog
    full_records_state = gr.State([])

    gr.HTML('<div class="dr-catalog-label">Research Catalog</div>')

    catalog_df = gr.Dataframe(
        headers=["#", "Date & Time", "User Query", "Research Output"],
        datatype=["number", "str", "str", "str"],
        interactive=False,
        elem_id="dr-catalog",
        value=[],
    )

    catalog_detail = gr.Markdown(elem_id="dr-catalog-detail", visible=False)

    def show_detail(evt: gr.SelectData, records):
        row = evt.index[0]
        if records and 0 <= row < len(records):
            return gr.update(value=records[row]["output"], visible=True)
        return gr.update(visible=False)

    catalog_df.select(show_detail, inputs=[full_records_state], outputs=[catalog_detail])

    ui.load(load_catalog, outputs=[catalog_df, full_records_state])

    run_button.click(run, inputs=[query_textbox], outputs=[report, catalog_df, full_records_state])
    query_textbox.submit(run, inputs=[query_textbox], outputs=[report, catalog_df, full_records_state])


def check_passcode(username: str, password: str) -> bool:
    return password == "6768"


if __name__ == "__main__":
    ui.launch(
        css=CSS,
        js=JS,
        theme=gr.themes.Base(),
        auth=check_passcode,
        auth_message="Enter any name and the passcode to access Deep Research.",
    )
