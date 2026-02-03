import ChatWindow from "./components/ChatWindow.jsx";
import React from "react";
import { useMessagePolling } from "../hooks/useMessagePolling.js";
import { useWebSocket } from "../hooks/useWebSocket.js";
import { API_CONFIG } from "./config/api.js";

function App() {
  const pollingHook = useMessagePolling();
  const websocketHook = useWebSocket();
  
  const { messages, setMessages, loading, error, handleSendMessage, isConnected } = 
    API_CONFIG.USE_WEBSOCKET ? websocketHook : pollingHook;

  const handleReactionChange = (updatedMessage) => {
    setMessages(prev => 
      prev.map(msg => msg.id === updatedMessage.id ? updatedMessage : msg)
    );
  };

  return (
    <div className="flex justify-center items-start min-h-screen bg-gray-100 p-6">
      <div className="w-full max-w-sm h-[700px] bg-white shadow-xl rounded-3xl flex flex-col overflow-hidden">
        {API_CONFIG.USE_WEBSOCKET && isConnected !== undefined && (
          <div className={`text-xs text-center py-1 ${isConnected ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
            {isConnected ? '🟢 Connected' : '🟡 Reconnecting...'}
          </div>
        )}
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

