import { useState, useEffect, useRef } from "react";
import { fetchMessages, postMessage, pollMessages } from "../src/utils/api.jsx";

export const useMessagePolling = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const lastIsoRef = useRef(null);

  useEffect(() => {
    let isMounted = true;
    
    const loadAndPoll = async () => {
      setLoading(true);
      setError(null);
     
      try {
        const data = await fetchMessages();
        if (!isMounted) return;
        
        const sortedData = [...data].reverse(); 
        setMessages(sortedData);
        
        if (data.length > 0 && data[0].timestamp_iso) {
          lastIsoRef.current = data[0].timestamp_iso;
        } else {
          lastIsoRef.current = new Date().toISOString();
        }
      } catch (err) {
        console.error("Error loading messages:", err);
        if (isMounted) setError("Failed to load messages");
        lastIsoRef.current = new Date().toISOString();
      } finally {
        if (isMounted) setLoading(false);
      }

      while (isMounted) {
        try {
            const newMsgs = await pollMessages(lastIsoRef.current);
            if (!isMounted) break;
            
            if (newMsgs.length > 0) {
                setMessages(prev => {
                  const existingIds = new Set(prev.map(m => m.id));
                  const uniqueNewMsgs = newMsgs.filter(m => !existingIds.has(m.id));
                  return [...prev, ...uniqueNewMsgs];
                });
  
                const lastMsg = newMsgs[newMsgs.length - 1];
                if (lastMsg.timestamp_iso) {
                    lastIsoRef.current = lastMsg.timestamp_iso;
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
        const response = await postMessage(newMessage);
        if (response?.timestamp_iso) {
          lastIsoRef.current = response.timestamp_iso;
        }
    } catch (err) {
        console.error("Failed to send", err);
    }
  };

  return {
    messages,
    setMessages,
    loading,
    error,
    handleSendMessage,
  };
};
