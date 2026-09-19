import sqlite3
from pathlib import Path
from flask import current_app, g

SCHEMA = Path(__file__).resolve().parent.parent / "database" / "schema.sql"

def get_db():
    if "db" not in g:
        path = Path(current_app.config["DATABASE"])
        path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    db.executescript(SCHEMA.read_text(encoding="utf-8"))
    db.commit()

def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
