/**
 * ChatWindow.jsx
 * --------------
 * Scrollable list of MessageBubble components. Auto-scrolls to the
 * bottom whenever a new message is added.
 */

import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble.jsx";

export default function ChatWindow({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: "16px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {messages.length === 0 && (
        <p style={{ color: "#9ca3af", fontSize: "14px", textAlign: "center" }}>
          Say hi to start the conversation.
        </p>
      )}
      {messages.map((m, i) => (
        <MessageBubble key={i} role={m.role} content={m.content} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
