import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image

from ..config import ENCRYPTED_DIR, KEYS_DIR, TEMP_DIR
from ..dependencies import get_current_user
from ..services.activity import ActivityLogger
from ..services.crypto import compute_integrity_hash, encrypt_with_visualization
from ..services.data import DataManager
from ..services.files import save_upload


router = APIRouter(prefix="/api/images", tags=["images"])


@router.post("/upload")
def upload_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    suffix = Path(file.filename or "upload.png").suffix
    temp_name = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{Path(file.filename or 'image').stem}{suffix}"
    temp_path = TEMP_DIR / temp_name
    save_upload(file, temp_path)
    return {"filename": file.filename, "temp_path": str(temp_path), "temp_url": DataManager.media_url(str(temp_path))}


@router.post("/encrypt")
def encrypt_image(
    file: UploadFile = File(...),
    x0: float = Form(0.654321),
    r: float = Form(3.99),
    beta: float = Form(3.0),
    lambda_val: int = Form(500),
    hidden_message: str | None = Form(default=None),
    current_user: dict = Depends(get_current_user),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported image type")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_root = Path(file.filename).stem
    temp_path = TEMP_DIR / f"{timestamp}_{file.filename}"
    enc_path = ENCRYPTED_DIR / f"enc_{timestamp}_{file_root}.png"
    key_path = KEYS_DIR / f"key_{timestamp}_{file_root}.npz"
    save_upload(file, temp_path)

    try:
        _, _, stage_images = encrypt_with_visualization(
            temp_path,
            x0,
            r,
            beta,
            lambda_val,
            enc_path,
            key_path,
            hidden_message=hidden_message if hidden_message else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    original_hash = compute_integrity_hash(temp_path, hidden_message=hidden_message if hidden_message else None)

    image_id = DataManager.save_image_metadata(
        f"{file_root}.png",
        enc_path,
        key_path,
        current_user["user_id"],
        x0,
        r,
        beta,
        lambda_val,
        original_hash=original_hash,
        has_hidden_msg=1 if hidden_message else 0,
    )
    ActivityLogger.log(current_user["user_id"], "ENCRYPT", f"Encrypted {file.filename}")

    stage_urls = {}
    for stage_name, stage_array in stage_images.items():
        stage_path = TEMP_DIR / f"viz_{stage_name}_{timestamp}_{file_root}.png"
        Image.fromarray(stage_array).save(stage_path, "PNG")
        stage_urls[stage_name] = DataManager.media_url(str(stage_path))

    return {
        "image_id": image_id,
        "filename": f"{file_root}.png",
        "encrypted_path": str(enc_path),
        "encrypted_url": DataManager.media_url(str(enc_path)),
        "key_path": str(key_path),
        "key_url": DataManager.media_url(str(key_path)),
        "original_hash": original_hash,
        "has_hidden_msg": 1 if hidden_message else 0,
        "visualization": {
            "steps": [
                {"id": "original", "title": "Step 1/8 - Loading image", "caption": "Original image", "image_url": stage_urls["original"]},
                {"id": "key_preview", "title": "Step 4/8 - Building chaotic key matrices", "caption": "Chaotic key matrix", "image_url": stage_urls["key_preview"]},
                {"id": "first_diffusion", "title": "Step 6/8 - First diffusion layer", "caption": "After first diffusion layer", "image_url": stage_urls["first_diffusion"]},
                {"id": "encrypted", "title": "Step 7/8 - Final encryption layer", "caption": "Fully encrypted", "image_url": stage_urls["encrypted"]},
            ]
        },
    }


@router.get("/")
def get_my_images(current_user: dict = Depends(get_current_user)):
    images = DataManager.get_user_images(current_user["user_id"]).to_dict(orient="records")
    for image in images:
        image["encrypted_url"] = DataManager.media_url(image["encrypted_path"])
        image["key_url"] = DataManager.media_url(image["key_path"])
    return {"images": images}


@router.get("/sent")
def get_sent_history(current_user: dict = Depends(get_current_user)):
    images = DataManager.get_user_images(current_user["user_id"]).to_dict(orient="records")
    for image in images:
        image["encrypted_url"] = DataManager.media_url(image["encrypted_path"])
        image["key_url"] = DataManager.media_url(image["key_path"])

    return {
        "images": images,
        "shared_history": DataManager.get_images_i_shared(current_user["user_id"]).to_dict(orient="records"),
    }
