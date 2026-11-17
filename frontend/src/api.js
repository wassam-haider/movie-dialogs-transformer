/**
 * api.js
 * ------
 * Every call to the FastAPI backend goes through here. Keeping fetch
 * calls in one file means the rest of the app never has to know the
 * backend's URL or JSON shape.
 */

const API_BASE = "http://localhost:8000";

export async function sendMessage(sessionId, message) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status}`);
  }

  return res.json(); // { session_id, reply }
}

export async function fetchHistory(sessionId) {
  const res = await fetch(`${API_BASE}/api/sessions/${sessionId}`);
  if (!res.ok) {
    throw new Error(`History request failed: ${res.status}`);
  }
  return res.json(); // { session_id, messages: [...] }
}
