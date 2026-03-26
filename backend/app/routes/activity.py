from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..services.data import DataManager


router = APIRouter(prefix="/api/activity", tags=["activity"])


@router.get("")
def get_activity(current_user: dict = Depends(get_current_user), limit: int = 50):
    return {"logs": DataManager.get_activity_logs(current_user["user_id"], limit).to_dict(orient="records")}
