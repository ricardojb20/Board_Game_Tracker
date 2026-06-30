from fastapi import FastAPI
from backend.routes.games import router as games_router
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent.parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/images",
    StaticFiles(directory=BASE_DIR / "images"),
    name="images"
)

app.include_router(games_router)


@app.get("/")
def home():
    return {"message": "API Board Game Tracker"}