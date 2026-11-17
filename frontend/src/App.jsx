/**
 * App.jsx
 * -------
 * Top-level component. Holds the message list and the session_id in
 * state, and wires the input box to the backend via api.js.
 *
 * The session_id is also saved to localStorage so refreshing the page
 * keeps you in the same conversation (the backend keeps the full
 * history in Postgres either way).
 */

import { useEffect, useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import ChatInput from "./components/ChatInput.jsx";
import { sendMessage, fetchHistory } from "./api.js";

const STORAGE_KEY = "movie_chatbot_session_id";

export default function App() {
  const [sessionId, setSessionId] = useState(() => localStorage.getItem(STORAGE_KEY));
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);

  // On first load, if we already have a session_id from a previous
  // visit, pull its history back from Postgres so the chat isn't empty.
  useEffect(() => {
    if (!sessionId) return;
    fetchHistory(sessionId)
      .then((data) => setMessages(data.messages))
      .catch(() => {
        // Session id was stale/invalid (e.g. DB was reset) — start fresh.
        localStorage.removeItem(STORAGE_KEY);
        setSessionId(null);
      });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  async function handleSend(text) {
    setError(null);
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setSending(true);

    try {
      const data = await sendMessage(sessionId, text);

      if (!sessionId) {
        localStorage.setItem(STORAGE_KEY, data.session_id);
        setSessionId(data.session_id);
      }

      setMessages((prev) => [...prev, { role: "bot", content: data.reply }]);
    } catch (err) {
      setError("Couldn't reach the backend. Is it running on localhost:8000?");
    } finally {
      setSending(false);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        maxWidth: "600px",
        margin: "0 auto",
        fontFamily: "system-ui, sans-serif",
        border: "1px solid #e5e7eb",
      }}
    >
      <header style={{ padding: "14px 16px", borderBottom: "1px solid #e5e7eb" }}>
        <h1 style={{ fontSize: "16px", margin: 0 }}>Movie Dialogs Chatbot</h1>
        <p style={{ fontSize: "12px", color: "#9ca3af", margin: "2px 0 0" }}>
          A Transformer trained from scratch on the Cornell Movie-Dialogs Corpus
        </p>
      </header>

      <ChatWindow messages={messages} />

      {error && (
        <p style={{ color: "#dc2626", fontSize: "12px", padding: "0 16px" }}>{error}</p>
      )}

      <ChatInput onSend={handleSend} disabled={sending} />
    </div>
  );
}
