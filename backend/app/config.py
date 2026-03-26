from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "dna_encryption.db"
ENCRYPTED_DIR = BASE_DIR / "encrypted_images"
KEYS_DIR = BASE_DIR / "keys"
TEMP_DIR = BASE_DIR / "temp"
MEDIA_DIRS = {
    "encrypted_images": ENCRYPTED_DIR,
    "keys": KEYS_DIR,
    "temp": TEMP_DIR,
}
