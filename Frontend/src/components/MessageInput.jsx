import { useState } from "react";
import React from "react";

function UsernameEntry({ onSend }) {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");
  const [scheduledFor, setScheduledFor] = useState("");
  const [textColor, setTextColor] = useState("#111827");
  const [isBold, setIsBold] = useState(false);
  const [isItalic, setIsItalic] = useState(false);

  const handleSend = (e) => {
    e?.preventDefault(); 
    if (username.trim() && message.trim()) {
      onSend({
        username,
        content: message,
        scheduled_for: scheduledFor || null,
        text_color: textColor,
        is_bold: isBold,
        is_italic: isItalic,
      });
      setMessage("");
      setScheduledFor("");
      setIsBold(false);
      setIsItalic(false);
      setTextColor("#3f568a");
    }
  }

  return (
    <form className="border-t p-3 bg-white flex flex-col gap-3" onSubmit={handleSend}>
      <div className="flex gap-2 items-center">
        <input
          className="w-1/3 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          type="text"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="flex-1 border rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
          type="text"
          placeholder="Enter your message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{ color: textColor, fontWeight: isBold ? "700" : "400", fontStyle: isItalic ? "italic" : "normal" }}
        />
      </div>

      <div className="flex flex-wrap gap-3 items-center text-sm text-gray-700">
        <label className="flex items-center gap-2">
          <span>Color</span>
          <input
            type="color"
            value={textColor}
            onChange={(e) => setTextColor(e.target.value)}
            className="w-10 h-10 p-1 rounded border"
          />
        </label>

        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={isBold}
            onChange={(e) => setIsBold(e.target.checked)}
          />
          <span className="font-semibold">Bold</span>
        </label>

        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={isItalic}
            onChange={(e) => setIsItalic(e.target.checked)}
          />
          <span className="italic">Italic</span>
        </label>

        <label className="flex items-center gap-2 ml-auto">
          <span>Schedule</span>
          <input
            type="datetime-local"
            value={scheduledFor}
            onChange={(e) => setScheduledFor(e.target.value)}
            className="border rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        </label>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
          disabled={!username.trim() || !message.trim()}
        >
          Send
        </button>
      </div>
    </form>
  );
}

export default UsernameEntry;