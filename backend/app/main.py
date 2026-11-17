"""
main.py
-------
The FastAPI application entry point.

What happens at startup (once, not per-request):
  1. The trained checkpoint is loaded into a ChatbotEngine and kept on
     app.state.engine for the life of the process.
  2. The two Postgres tables (chat_sessions, chat_messages) are created
     on your Neon database if they don't already exist.

Run this with:
  uvicorn app.main:app --reload --port 8000
(from inside backend/, with your venv active — see COMMANDS.txt)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CHECKPOINT_PATH, FRONTEND_ORIGIN, DEVICE
from .database import Base, engine
from .inference import ChatbotEngine
from .routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    print(f"Loading model from {CHECKPOINT_PATH} onto {DEVICE} ...")
    app.state.engine = ChatbotEngine(CHECKPOINT_PATH, device=DEVICE)

    print("Ensuring Postgres tables exist ...")
    Base.metadata.create_all(bind=engine)

    yield
    # ---- shutdown ---- (nothing to clean up for this simple app)


app = FastAPI(title="Movie Dialogs Chatbot API", lifespan=lifespan)

# Allows the React dev server (default http://localhost:5173) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Movie Dialogs Chatbot API is running"}
