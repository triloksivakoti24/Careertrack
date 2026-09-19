import sqlite3
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "applications.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def ensure_data_directory() -> None:
    """Create the data directory if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """
    Create and return a configured SQLite database connection.
    """
    ensure_data_directory()

    connection = sqlite3.connect(
        DB_PATH,
        timeout=10,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA busy_timeout = 10000")

    return connection


def initialize_database() -> None:
    """
    Initialize the database using the SQL schema file.
    """
    ensure_data_directory()

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Database schema file not found: {SCHEMA_PATH}"
        )

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as connection:
        connection.executescript(schema_sql)
        connection.commit()


def execute_query(
    query: str,
    parameters: tuple = (),
) -> sqlite3.Cursor:
    """
    Execute INSERT, UPDATE, or DELETE queries.
    """
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        connection.commit()
        return cursor


def fetch_one(
    query: str,
    parameters: tuple = (),
) -> Optional[sqlite3.Row]:
    """
    Fetch a single database row.
    """
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchone()


def fetch_all(
    query: str,
    parameters: tuple = (),
) -> list[sqlite3.Row]:
    """
    Fetch multiple database rows.
    """
    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchall()


# Initialize database automatically when this module is imported.
initialize_database()