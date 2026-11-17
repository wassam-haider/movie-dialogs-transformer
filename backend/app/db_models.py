"""
db_models.py
------------
The two tables this app needs:

- chat_sessions: one row per browser tab/visitor session.
- chat_messages: one row per message, user or bot, linked to a session.

Base.metadata.create_all() (called from main.py on startup) creates
these automatically the first time you run the app — no manual
migration step needed for a project this size.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=_new_uuid)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=_new_uuid)
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    role = Column(String, nullable=False)       # "user" or "bot"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=_utcnow)

    session = relationship("ChatSession", back_populates="messages")
