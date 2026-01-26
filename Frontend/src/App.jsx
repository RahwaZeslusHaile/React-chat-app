import { fetchMessages, postMessage, pollMessages } from "./utils/api.jsx";
import ChatWindow from "./components/ChatWindow.jsx";
import React, { useState, useEffect } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    
    const loadAndPoll = async () => {
      setLoading(true);
      setError(null);
     
      let lastIso;
      try {
        const data = await fetchMessages();
        if (!isMounted) return;
        
        const sortedData = [...data].reverse(); 
        setMessages(sortedData);
        
        if (data.length > 0 && data[0].timestamp_iso) {
          lastIso = data[0].timestamp_iso;
        } else {
          lastIso = new Date().toISOString();
        }
      } catch (err) {
        console.error("Error loading messages:", err);
        if (isMounted) setError("Failed to load messages");
        lastIso = new Date().toISOString();
      } finally {
        if (isMounted) setLoading(false);
      }

      while (isMounted) {
        try {
            const newMsgs = await pollMessages(lastIso);
            if (!isMounted) break;
            
            if (newMsgs.length > 0) {
                setMessages(prev => {
                  const existingIds = new Set(prev.map(m => m.id));
                  const uniqueNewMsgs = newMsgs.filter(m => !existingIds.has(m.id));
                  return [...prev, ...uniqueNewMsgs];
                });
  
                const lastMsg = newMsgs[newMsgs.length - 1];
                if (lastMsg.timestamp_iso) {
                    lastIso = lastMsg.timestamp_iso;
                }
            }
        } catch (pollingErr) {
            console.error("Polling loop error", pollingErr);
            await new Promise(r => setTimeout(r, 2000));
        }
      }
    };

    loadAndPoll();

    return () => {
      isMounted = false;
    };
  }, []);

  const handleSendMessage = async (newMessage) => {
    try {
        await postMessage(newMessage);
    } catch (err) {
        console.error("Failed to send", err);
    }
  };

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

