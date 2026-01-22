import { fetchMessages, postMessage } from "./utilis/api.js";
import ChatWindow from "./components/ChatWindow.js";
import React, { useState, useEffect } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

 
  useEffect(() => {
    const loadMessages = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await fetchMessages();
        setMessages(data); 
      } catch (err) {
        console.error("Error loading messages:", err);
        setError("Failed to load messages");
        setMessages([]); 
      } finally {
        setLoading(false);
      }
    };

    loadMessages();
  }, []);

 
  const handleSendMessage = async (newMessage) => {
    const savedMessage = await postMessage(newMessage);
    if (!savedMessage) return; 
    setMessages((prevMessages) => [
      ...(Array.isArray(prevMessages) ? prevMessages : []),
      savedMessage,
    ]);
  };

  return (
    <div className="flex justify-center items-start min-h-screen bg-gray-100 p-6">
      <div className="w-full max-w-sm h-[700px] bg-white shadow-xl rounded-3xl flex flex-col overflow-hidden">
        {loading ? (
          <p className="m-auto text-gray-500">Loading messages...</p>
        ) : error ? (
          <p className="m-auto text-red-500">{error}</p>
        ) : (
          <ChatWindow messages={messages} onSendMessage={handleSendMessage} />
        )}
      </div>
    </div>
  );
}

export default App;
