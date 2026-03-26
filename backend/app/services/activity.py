from ..database import get_connection


class ActivityLogger:
    @staticmethod
    def log(user_id, action, details=""):
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO activity_logs (user_id, action, details) VALUES (?, ?, ?)",
                (user_id, action, details),
            )
