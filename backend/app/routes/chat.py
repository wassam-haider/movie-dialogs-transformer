"""
routes/chat.py
--------------
The two endpoints the frontend talks to:

  POST /api/chat                     -> send a message, get a reply
  GET  /api/sessions/{session_id}    -> fetch the full history for that session

The actual model call happens through app.state.engine (set once at
startup in main.py) — routes never touch the checkpoint directly.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..db_models import ChatSession, ChatMessage
from ..schemas import ChatRequest, ChatResponse, HistoryResponse

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def send_message(payload: ChatRequest, request: Request, db: Session = Depends(get_db)):
    engine = request.app.state.engine  # the loaded ChatbotEngine, set at startup

    # First message of a conversation: create a new session row.
    # Otherwise: look up the existing one (404 if the id is bogus).
    if payload.session_id:
        session = db.get(ChatSession, payload.session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="Unknown session_id")
    else:
        session = ChatSession()
        db.add(session)
        db.flush()  # assigns session.id without committing yet

    # Save the user's message.
    db.add(ChatMessage(session_id=session.id, role="user", content=payload.message))

    # Run the model.
    reply_text = engine.generate_reply(payload.message)

    # Save the bot's reply.
    db.add(ChatMessage(session_id=session.id, role="bot", content=reply_text))

    db.commit()

    return ChatResponse(session_id=session.id, reply=reply_text)


@router.get("/sessions/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str, db: Session = Depends(get_db)):
    session = db.get(ChatSession, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Unknown session_id")

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )
    return HistoryResponse(session_id=session_id, messages=messages)
