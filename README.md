# Movie Dialogs Chatbot

A chatbot wrapper around a Transformer (encoder-decoder, Vaswani et al. 2017
architecture, ~13.5M parameters) trained from scratch on the Cornell
Movie-Dialogs Corpus. Runs entirely on your own laptop — React frontend,
FastAPI backend, CPU inference — with chat history stored in a free
Neon Postgres database in the cloud.

## Why this design

- **No GPU needed.** The model is small enough (13.5M params) that CPU
  inference on a normal laptop takes well under a second per reply.
- **Nothing hosted.** Frontend and backend both run locally on
  `localhost`; only the database lives online (Neon's free tier),
  which is what lets chat history survive you restarting the app.
- **Same architecture as training, unchanged.** `backend/app/transformer_model.py`
  is copied verbatim from the training notebook so the saved checkpoint's
  weights load in without any shape mismatches.

## Project structure

```
movie-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app + startup model loading
│   │   ├── config.py            # reads .env (DB url, checkpoint path)
│   │   ├── transformer_model.py # model architecture (matches training notebook)
│   │   ├── tokenizer.py         # text cleaning + encode/decode
│   │   ├── inference.py         # loads checkpoint, greedy decode loop
│   │   ├── database.py          # SQLAlchemy engine/session
│   │   ├── db_models.py         # ChatSession, ChatMessage tables
│   │   ├── schemas.py           # Pydantic request/response models
│   │   └── routes/
│   │       └── chat.py          # POST /api/chat, GET /api/sessions/{id}
│   ├── checkpoints/              # put your best_model.pt here (not in git)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # top-level component, session handling
│   │   ├── api.js                # fetch() calls to the backend
│   │   └── components/
│   │       ├── ChatWindow.jsx
│   │       ├── MessageBubble.jsx
│   │       └── ChatInput.jsx
│   └── package.json
├── COMMANDS.txt                  # every terminal command, in order
├── LINKEDIN_POSTS.md             # draft posts for the two-part series
└── .gitignore
```

## How a message flows through the app

1. React sends `{ session_id, message }` to `POST /api/chat`.
2. FastAPI validates it with the `ChatRequest` Pydantic model.
3. `tokenizer.py` cleans the text and turns it into token ids using the
   **vocab saved inside the checkpoint** — not rebuilt, so it's guaranteed
   to match what the model was trained on.
4. `inference.py` runs the encoder once, then autoregressively decodes
   one token at a time (feeding each prediction back in) until it
   produces `<eos>` or hits `max_seq_length`.
5. The user's message and the bot's reply are both written to Postgres
   (`chat_messages` table, linked to a `chat_sessions` row).
6. The reply is returned as JSON and rendered as a new bubble in the UI.

## Before you run it

- **Get the checkpoint into the project.** Copy `best_model.pt` (or
  whichever epoch you want) from your downloaded zip into
  `backend/checkpoints/`.
- **Create a free Neon Postgres database** at https://neon.tech, then
  copy its connection string — you'll need it for `backend/.env`.
- Full step-by-step commands are in `COMMANDS.txt`.

## A note on the model itself

This checkpoint was trained for 10 epochs and validation loss was still
around 7.2 — that's early-stage for this architecture (a well-converged
run on this dataset usually gets well under 3). In practice this means
replies will often be short, repetitive, or generic right now. The
chatbot wrapper works correctly regardless — if you train longer or
tweak hyperparameters, just drop the new checkpoint into
`backend/checkpoints/` and restart the backend, no other code changes
needed.
