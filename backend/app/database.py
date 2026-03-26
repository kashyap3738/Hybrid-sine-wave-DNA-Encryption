import sqlite3
from contextlib import contextmanager

from .config import DATABASE_PATH


@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_database():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS images (
                image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                encrypted_path TEXT NOT NULL,
                key_path TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                x0 REAL,
                r REAL,
                beta REAL,
                lambda_val REAL,
                original_hash TEXT,
                has_hidden_msg INTEGER DEFAULT 0,
                FOREIGN KEY (owner_id) REFERENCES users(user_id)
            )"""
        )

        try:
            cursor.execute("ALTER TABLE images ADD COLUMN original_hash TEXT")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE images ADD COLUMN has_hidden_msg INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS shares (
                share_id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id INTEGER NOT NULL,
                sender_id INTEGER NOT NULL,
                receiver_id INTEGER NOT NULL,
                shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                view_duration INTEGER DEFAULT NULL,
                is_expired INTEGER DEFAULT 0,
                FOREIGN KEY (image_id) REFERENCES images(image_id),
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (receiver_id) REFERENCES users(user_id),
                UNIQUE(image_id, receiver_id)
            )"""
        )

        try:
            cursor.execute("ALTER TABLE shares ADD COLUMN view_duration INTEGER DEFAULT NULL")
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("ALTER TABLE shares ADD COLUMN is_expired INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS activity_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )"""
        )
