from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_current_user
from ..schemas import ChangePasswordRequest, LoginRequest, RegisterRequest
from ..security import create_token
from ..services.activity import ActivityLogger
from ..services.auth import AuthManager


router = APIRouter(prefix="/api/auth", tags=["auth"])


def validate_registration_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long.")
    if not any(c.islower() for c in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must include at least one lowercase letter.")
    if not any(c.isupper() for c in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must include at least one uppercase letter.")
    if not any(c.isdigit() for c in password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must include at least one number.")


@router.post("/login")
def login(payload: LoginRequest):
    user = AuthManager.authenticate(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials. Please try again.")

    ActivityLogger.log(user["user_id"], "LOGIN", f"User {payload.username} logged in")
    return {"token": create_token(user["user_id"], user["username"]), "user": user}


@router.post("/register")
def register(payload: RegisterRequest):
    if not payload.username or not payload.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill in both fields.")
    validate_registration_password(payload.password)
    success, msg = AuthManager.register_user(payload.username, payload.password)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)
    return {"message": msg}


@router.post("/change-password")
def change_password(payload: ChangePasswordRequest, current_user: dict = Depends(get_current_user)):
    if not payload.current_password or not payload.new_password or not payload.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please fill in all password fields.")
    if payload.new_password != payload.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New passwords do not match.")
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 6 characters.")

    ok, msg = AuthManager.change_password(current_user["user_id"], payload.current_password, payload.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    ActivityLogger.log(current_user["user_id"], "PASSWORD_CHANGE", f"{current_user['username']} changed their password")
    return {"message": msg}


@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    ActivityLogger.log(current_user["user_id"], "LOGOUT", f"User {current_user['username']} logged out")
    return {"message": "Logged out successfully"}
