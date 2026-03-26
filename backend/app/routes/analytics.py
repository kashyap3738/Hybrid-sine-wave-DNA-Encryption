import hashlib

import numpy as np
from fastapi import APIRouter, Depends, HTTPException, status
from PIL import Image

from ..config import TEMP_DIR
from ..dependencies import get_current_user
from ..services.crypto import decrypt_image_robust
from ..services.data import DataManager


router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def calculate_entropy(values):
    histogram, _ = np.histogram(values, bins=256, range=[0, 256], density=False)
    probabilities = histogram / np.sum(histogram)
    probabilities = probabilities[probabilities > 0]
    return float(-np.sum(probabilities * np.log2(probabilities)))


@router.get("/{image_id}")
def get_analytics(image_id: int, current_user: dict = Depends(get_current_user)):
    image = DataManager.get_image_by_id(image_id)
    if not image or image["owner_id"] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    proof_dec_path = TEMP_DIR / f"proof_{image['filename']}"

    try:
        decrypt_image_robust(image["encrypted_path"], image["key_path"], proof_dec_path)
        orig_img = Image.open(proof_dec_path).convert("RGB")
        enc_img = Image.open(image["encrypted_path"]).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Analysis failed: {exc}") from exc

    orig_array = np.array(orig_img).flatten()
    enc_array = np.array(enc_img).flatten()
    orig_hist, _ = np.histogram(orig_array, bins=256, range=[0, 256])
    enc_hist, _ = np.histogram(enc_array, bins=256, range=[0, 256])
    abs_difference = np.abs(orig_array.astype(np.int16) - enc_array.astype(np.int16))
    changed_pixels = int(np.count_nonzero(orig_array != enc_array))
    total_pixels = int(orig_array.size)

    decrypted_hash = hashlib.sha256(np.array(orig_img).tobytes()).hexdigest()
    stored_hash = image["original_hash"]
    integrity_status = "MATCH" if stored_hash and stored_hash == decrypted_hash else "UNKNOWN" if not stored_hash else "FAILED"
    original_entropy = calculate_entropy(orig_array)
    encrypted_entropy = calculate_entropy(enc_array)

    return {
        "image_id": image_id,
        "histogram": {
            "labels": list(range(256)),
            "original": orig_hist.tolist(),
            "encrypted": enc_hist.tolist(),
        },
        "comparison": {
            "original_mean": float(np.mean(orig_array)),
            "encrypted_mean": float(np.mean(enc_array)),
            "original_std": float(np.std(orig_array)),
            "encrypted_std": float(np.std(enc_array)),
            "mean_absolute_difference": float(np.mean(abs_difference)),
            "changed_pixel_ratio": float(changed_pixels / total_pixels),
        },
        "entropy": {
            "original": round(original_entropy, 4),
            "encrypted": round(encrypted_entropy, 4),
            "max": 8.0,
            "randomness_score": round((encrypted_entropy / 8.0) * 100, 2),
        },
        "integrity": {
            "stored_hash": stored_hash,
            "decrypted_hash": decrypted_hash,
            "status": integrity_status,
            "is_match": integrity_status == "MATCH",
        },
    }
