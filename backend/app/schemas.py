from typing import Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str


class ShareRequest(BaseModel):
    image_id: int
    receiver_id: int
    view_duration: Optional[int] = Field(default=None, ge=1, le=300)
