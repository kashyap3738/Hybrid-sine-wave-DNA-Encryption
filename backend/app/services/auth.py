import sqlite3

from ..database import get_connection
from ..security import hash_password


class AuthManager:
    @staticmethod
    def authenticate(username, password):
        with get_connection() as conn:
            user = conn.execute(
                "SELECT user_id, username FROM users WHERE username=? AND password_hash=? AND is_active=1",
                (username, hash_password(password)),
            ).fetchone()
        if user:
            return {"user_id": user["user_id"], "username": user["username"]}
        return None

    @staticmethod
    def register_user(username, password):
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, hash_password(password)),
                )
            return True, "User registered successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    @staticmethod
    def change_password(user_id, current_password, new_password):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT user_id FROM users WHERE user_id=? AND password_hash=?",
                (user_id, hash_password(current_password)),
            ).fetchone()
            if not row:
                return False, "Current password is incorrect."

            conn.execute(
                "UPDATE users SET password_hash=? WHERE user_id=?",
                (hash_password(new_password), user_id),
            )
        return True, "Password updated successfully."
