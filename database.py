import sqlite3
from contextlib import contextmanager

DB_PATH = 'vocab.db'

@contextmanager
def get_connection():
    """Context manager that opens a DB connection and guarantees it is closed."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                word TEXT NOT NULL,
                translation TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        conn.commit()


def add_word(user_id: int, word: str, translation: str) -> None:
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO words (user_id, word, translation) VALUES (?, ?, ?)',
            (user_id, word.strip(), translation.strip())
        )
        conn.commit()


def get_words(user_id: int) -> list[tuple]:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT word, translation FROM words WHERE user_id = ?',
            (user_id,)
        )
        return cursor.fetchall()


def get_random_word(user_id: int) -> tuple | None:
    with get_connection() as conn:
        cursor = conn.execute(
            'SELECT word, translation FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 1',
            (user_id,)
        )
        return cursor.fetchone()
