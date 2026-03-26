from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..services.data import DataManager


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user, "stats": DataManager.get_user_stats(current_user["user_id"])}


@router.get("")
def get_users(current_user: dict = Depends(get_current_user)):
    return {"users": DataManager.get_all_users().to_dict(orient="records")}


@router.get("/others")
def get_other_users(current_user: dict = Depends(get_current_user)):
    return {"users": DataManager.get_other_users(current_user["user_id"]).to_dict(orient="records")}
