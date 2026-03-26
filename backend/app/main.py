from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import ENCRYPTED_DIR, KEYS_DIR, TEMP_DIR
from .database import init_database
from .routes import activity, analytics, auth, images, shares, users
from .services.files import init_directories


app = FastAPI(title="DNA Encryption API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# StaticFiles validates directories at import time, so initialize them before mounting.
init_directories()
init_database()


@app.on_event("startup")
def startup():
    init_directories()
    init_database()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(images.router)
app.include_router(shares.router)
app.include_router(analytics.router)
app.include_router(activity.router)

app.mount("/media/encrypted_images", StaticFiles(directory=ENCRYPTED_DIR), name="encrypted-images")
app.mount("/media/keys", StaticFiles(directory=KEYS_DIR), name="keys")
app.mount("/media/temp", StaticFiles(directory=TEMP_DIR), name="temp")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
