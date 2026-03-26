import hashlib
import hmac
import os
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode

from fastapi import HTTPException, status


SECRET_KEY = os.environ.get("DNA_APP_SECRET", "development-secret-change-me")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_token(user_id: int, username: str) -> str:
    issued_at = str(int(time.time()))
    payload = f"{user_id}:{username}:{issued_at}"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return urlsafe_b64encode(f"{payload}:{signature}".encode()).decode()


def decode_token(token: str) -> dict:
    try:
        raw = urlsafe_b64decode(token.encode()).decode()
        user_id, username, issued_at, signature = raw.split(":", 3)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    payload = f"{user_id}:{username}:{issued_at}"
    expected = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return {"user_id": int(user_id), "username": username}
