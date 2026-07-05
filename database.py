import sqlite3

DB_PATH = "research_catalog.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS research_catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_query TEXT NOT NULL,
                research_output TEXT NOT NULL
            )
        """)


def save_research(query: str, output: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO research_catalog (user_query, research_output) VALUES (?, ?)",
            (query, output),
        )


def get_all_research():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(
            "SELECT id, created_at, user_query, research_output "
            "FROM research_catalog ORDER BY created_at DESC"
        ).fetchall()
