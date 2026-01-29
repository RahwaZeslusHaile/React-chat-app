import ChatWindow from "./components/ChatWindow.jsx";
import React from "react";
import { useMessagePolling } from "../hooks/useMessagePolling.js";

function App() {
  const { messages, setMessages, loading, error, handleSendMessage } = useMessagePolling();

  const handleReactionChange = (updatedMessage) => {
    setMessages(prev => 
      prev.map(msg => msg.id === updatedMessage.id ? updatedMessage : msg)
    );
  };

  return (
    <div className="flex justify-center items-start min-h-screen bg-gray-100 p-6">
      <div className="w-full max-w-sm h-[700px] bg-white shadow-xl rounded-3xl flex flex-col overflow-hidden">
        {loading ? (
          <p className="m-auto text-gray-500">Loading messages...</p>
        ) : error ? (
          <p className="m-auto text-red-500">{error}</p>
        ) : (
          <ChatWindow 
            messages={messages} 
            onSendMessage={handleSendMessage}
            onReactionChange={handleReactionChange}
          />
        )}
      </div>
    </div>
  );
}

export default App;

