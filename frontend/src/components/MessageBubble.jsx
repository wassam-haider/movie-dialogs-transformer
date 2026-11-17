/**
 * MessageBubble.jsx
 * -----------------
 * Renders a single chat message. `role` is either "user" or "bot" and
 * decides which side of the screen the bubble sits on.
 */

export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "8px",
      }}
    >
      <div
        style={{
          maxWidth: "70%",
          padding: "10px 14px",
          borderRadius: "14px",
          backgroundColor: isUser ? "#2563eb" : "#e5e7eb",
          color: isUser ? "#ffffff" : "#111827",
          fontSize: "14px",
          lineHeight: 1.4,
          whiteSpace: "pre-wrap",
        }}
      >
        {content}
      </div>
    </div>
  );
}
