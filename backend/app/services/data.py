import os
import threading
import time
from pathlib import Path

import pandas as pd

from ..database import get_connection


class DataManager:
    @staticmethod
    def save_image_metadata(
        filename,
        enc_path,
        key_path,
        owner_id,
        x0,
        r,
        beta,
        lambda_val,
        original_hash=None,
        has_hidden_msg=0,
    ):
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO images
                   (filename, encrypted_path, key_path, owner_id, x0, r, beta, lambda_val, original_hash, has_hidden_msg)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    filename,
                    str(enc_path),
                    str(key_path),
                    owner_id,
                    x0,
                    r,
                    beta,
                    lambda_val,
                    original_hash,
                    has_hidden_msg,
                ),
            )
            return cursor.lastrowid

    @staticmethod
    def get_user_images(user_id):
        with get_connection() as conn:
            return pd.read_sql_query(
                """SELECT image_id, filename, encrypted_path, key_path, uploaded_at, original_hash, has_hidden_msg
                   FROM images WHERE owner_id = ? ORDER BY uploaded_at DESC""",
                conn,
                params=(user_id,),
            )

    @staticmethod
    def get_all_users():
        with get_connection() as conn:
            return pd.read_sql_query(
                "SELECT user_id, username, created_at FROM users WHERE is_active=1",
                conn,
            )

    @staticmethod
    def get_other_users(exclude_user_id):
        with get_connection() as conn:
            return pd.read_sql_query(
                "SELECT user_id, username FROM users WHERE is_active=1 AND user_id != ?",
                conn,
                params=(exclude_user_id,),
            )

    @staticmethod
    def share_image_directly(image_id, sender_id, receiver_id, view_duration=None):
        try:
            with get_connection() as conn:
                conn.execute(
                    """INSERT INTO shares (image_id, sender_id, receiver_id, view_duration)
                       VALUES (?, ?, ?, ?)""",
                    (image_id, sender_id, receiver_id, view_duration),
                )
            return True, "Image shared successfully"
        except Exception as exc:
            if "UNIQUE constraint failed" in str(exc):
                return False, "Already shared with this user"
            raise

    @staticmethod
    def get_shared_with_me(receiver_id):
        with get_connection() as conn:
            return pd.read_sql_query(
                """SELECT s.share_id, s.image_id, i.filename, i.encrypted_path, i.key_path,
                          u.username as sender, s.shared_at, i.original_hash, i.has_hidden_msg,
                          s.view_duration, s.is_expired
                   FROM shares s
                   JOIN images i ON s.image_id = i.image_id
                   JOIN users u ON s.sender_id = u.user_id
                   WHERE s.receiver_id = ?
                   ORDER BY s.is_expired ASC, s.shared_at DESC""",
                conn,
                params=(receiver_id,),
            )

    @staticmethod
    def expire_share(share_id, dec_path=None):
        with get_connection() as conn:
            conn.execute("UPDATE shares SET is_expired = 1 WHERE share_id = ?", (share_id,))
        if dec_path and os.path.exists(dec_path):
            try:
                os.remove(dec_path)
            except Exception:
                pass

    @staticmethod
    def expire_share_delayed(share_id, dec_path, delay):
        time.sleep(delay)
        DataManager.expire_share(share_id, dec_path)

    @staticmethod
    def schedule_expiry(share_id, dec_path, delay):
        threading.Thread(
            target=DataManager.expire_share_delayed,
            args=(share_id, dec_path, delay),
            daemon=True,
        ).start()

    @staticmethod
    def get_user_stats(user_id):
        with get_connection() as conn:
            total_encrypted = conn.execute("SELECT COUNT(*) FROM images WHERE owner_id=?", (user_id,)).fetchone()[0]
            total_sent = conn.execute("SELECT COUNT(*) FROM shares WHERE sender_id=?", (user_id,)).fetchone()[0]
            total_received = conn.execute("SELECT COUNT(*) FROM shares WHERE receiver_id=?", (user_id,)).fetchone()[0]
            row = conn.execute("SELECT created_at FROM users WHERE user_id=?", (user_id,)).fetchone()
        return {
            "total_encrypted": total_encrypted,
            "total_sent": total_sent,
            "total_received": total_received,
            "created_at": row[0] if row else "Unknown",
        }

    @staticmethod
    def get_images_i_shared(sender_id):
        with get_connection() as conn:
            return pd.read_sql_query(
                """SELECT i.filename, u.username as shared_with, s.shared_at
                   FROM shares s
                   JOIN images i ON s.image_id = i.image_id
                   JOIN users u ON s.receiver_id = u.user_id
                   WHERE s.sender_id = ?
                   ORDER BY s.shared_at DESC""",
                conn,
                params=(sender_id,),
            )

    @staticmethod
    def get_activity_logs(user_id=None, limit=50):
        with get_connection() as conn:
            if user_id:
                return pd.read_sql_query(
                    """SELECT l.timestamp, u.username, l.action, l.details
                       FROM activity_logs l
                       LEFT JOIN users u ON l.user_id = u.user_id
                       WHERE l.user_id = ?
                       ORDER BY l.timestamp DESC
                       LIMIT ?""",
                    conn,
                    params=(user_id, limit),
                )
            return pd.read_sql_query(
                """SELECT l.timestamp, u.username, l.action, l.details
                   FROM activity_logs l
                   LEFT JOIN users u ON l.user_id = u.user_id
                   ORDER BY l.timestamp DESC
                   LIMIT ?""",
                conn,
                params=(limit,),
            )

    @staticmethod
    def get_image_by_id(image_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM images WHERE image_id = ?", (image_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_share_for_receiver(share_id, receiver_id):
        with get_connection() as conn:
            row = conn.execute(
                """SELECT s.share_id, s.image_id, i.filename, i.encrypted_path, i.key_path, s.view_duration, s.is_expired,
                          u.username as sender, i.has_hidden_msg
                   FROM shares s
                   JOIN images i ON s.image_id = i.image_id
                   JOIN users u ON s.sender_id = u.user_id
                   WHERE s.share_id = ? AND s.receiver_id = ?""",
                (share_id, receiver_id),
            ).fetchone()
        return dict(row) if row else None

    @staticmethod
    def media_url(path_str: str):
        path = Path(path_str)
        return f"/media/{path.parent.name}/{path.name}"
