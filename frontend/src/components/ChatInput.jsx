/**
 * ChatInput.jsx
 * -------------
 * Text box + send button. Enter also sends, same as any chat app.
 */

import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  function handleSend() {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
  }

  return (
    <div style={{ display: "flex", padding: "12px", borderTop: "1px solid #e5e7eb" }}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder={disabled ? "Waiting for a reply..." : "Type a message..."}
        disabled={disabled}
        style={{
          flex: 1,
          padding: "10px 12px",
          borderRadius: "8px",
          border: "1px solid #d1d5db",
          fontSize: "14px",
          outline: "none",
        }}
      />
      <button
        onClick={handleSend}
        disabled={disabled}
        style={{
          marginLeft: "8px",
          padding: "10px 18px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: disabled ? "#93c5fd" : "#2563eb",
          color: "#fff",
          fontSize: "14px",
          cursor: disabled ? "default" : "pointer",
        }}
      >
        Send
      </button>
    </div>
  );
}
