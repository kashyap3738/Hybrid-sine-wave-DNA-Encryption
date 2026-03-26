from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .database import get_connection
from .security import decode_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    token_data = decode_token(credentials.credentials)
    with get_connection() as conn:
        row = conn.execute(
            "SELECT user_id, username FROM users WHERE user_id=? AND is_active=1",
            (token_data["user_id"],),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return {"user_id": row["user_id"], "username": row["username"]}
