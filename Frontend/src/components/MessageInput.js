import { useState } from "react";
import React from "react";

function UsernameEntry({ onSend }) {
  const [username, setUsername] = useState("");
  const [message, setMessage] = useState("");
  const handleSend = () => {
    if (username.trim() && message.trim()) {
      onSend({ username: username, content: message, timeStamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
      setMessage("");
    }
}
    return (
        <div className="border-t p-3 bg-white flex gap-2 items-center">
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
  />
  <button
    className="bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"
    onClick={handleSend}
  >
    Send
  </button>
</div>
 
    );
}

export default UsernameEntry;