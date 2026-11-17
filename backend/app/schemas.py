"""
schemas.py
----------
Pydantic models — these validate every request that comes in and
shape every response that goes out. FastAPI uses them to auto-generate
the /docs page too.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    # None on the very first message of a new conversation; the
    # frontend then stores the session_id it gets back and sends it
    # on every message after that.
    session_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=500)


class ChatResponse(BaseModel):
    session_id: str
    reply: str


class MessageOut(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # lets this be built straight from a SQLAlchemy row


class HistoryResponse(BaseModel):
    session_id: str
    messages: list[MessageOut]
