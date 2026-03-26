import datetime
import time

from fastapi import APIRouter, Depends, HTTPException, status

from ..config import TEMP_DIR
from ..dependencies import get_current_user
from ..services.activity import ActivityLogger
from ..services.crypto import decrypt_image_robust
from ..services.data import DataManager
from ..schemas import ShareRequest


router = APIRouter(prefix="/api/shares", tags=["shares"])


@router.post("/")
def share_image(payload: ShareRequest, current_user: dict = Depends(get_current_user)):
    success, msg = DataManager.share_image_directly(
        payload.image_id,
        current_user["user_id"],
        payload.receiver_id,
        view_duration=payload.view_duration,
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    others = DataManager.get_other_users(current_user["user_id"])
    receiver_row = others[others["user_id"] == payload.receiver_id]
    receiver_name = receiver_row.iloc[0]["username"] if not receiver_row.empty else str(payload.receiver_id)
    ActivityLogger.log(current_user["user_id"], "SHARE", f"Shared image with {receiver_name}")
    return {"message": msg}


@router.get("/received")
def get_received(current_user: dict = Depends(get_current_user)):
    shares = DataManager.get_shared_with_me(current_user["user_id"]).to_dict(orient="records")
    for share in shares:
        share["encrypted_url"] = DataManager.media_url(share["encrypted_path"])
        share["key_url"] = DataManager.media_url(share["key_path"])
    return {"shares": shares}


@router.post("/{share_id}/decrypt")
def decrypt_shared_image(share_id: int, current_user: dict = Depends(get_current_user)):
    row = DataManager.get_share_for_receiver(share_id, current_user["user_id"])
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shared image not found")
    if row["is_expired"] == 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Self-Destructed: Time expired.")

    dec_path = TEMP_DIR / f"decrypted_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{row['filename']}"

    try:
        _, extracted_msg = decrypt_image_robust(row["encrypted_path"], row["key_path"], dec_path)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Decryption failed: {exc}") from exc

    ActivityLogger.log(current_user["user_id"], "DECRYPT", f"Decrypted {row['filename']} from {row['sender']}")

    expires_at = None
    if row["view_duration"]:
        expires_at = int(time.time()) + int(row["view_duration"])
        DataManager.schedule_expiry(row["share_id"], str(dec_path), int(row["view_duration"]))

    return {
        "share_id": row["share_id"],
        "filename": row["filename"],
        "sender": row["sender"],
        "decrypted_path": str(dec_path),
        "decrypted_url": DataManager.media_url(str(dec_path)),
        "hidden_message": extracted_msg,
        "has_hidden_msg": row["has_hidden_msg"],
        "view_duration": row["view_duration"],
        "expires_at": expires_at,
    }
