# FastAPI Backend

## Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Notes

- SQLite database file remains at the project root: `dna_encryption.db`
- Media directories remain at the project root:
  - `encrypted_images/`
  - `keys/`
  - `temp/`
- Static files are exposed under:
  - `/media/encrypted_images/...`
  - `/media/keys/...`
  - `/media/temp/...`
