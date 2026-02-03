import { useState, useEffect, useCallback } from "react";
import { wsClient } from "../src/services/websocket/wsClient.js";
import { postMessage } from "../src/utils/api.jsx";

export const useWebSocket = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    wsClient.connect();

    const unsubscribeMessages = wsClient.onMessage((data) => {
      switch (data.type) {
        case "messages_list": {
          const sortedData = [...data.data].reverse();
          setMessages(sortedData);
          setLoading(false);
          break;
        }

        case "new_message":
          setMessages((prev) => {
            const exists = prev.some((m) => m.id === data.data.id);
            if (!exists) {
              return [...prev, data.data];
            }
            return prev;
          });
          break;

        case "new_reply":
          setMessages((prev) => {
            const exists = prev.some((m) => m.id === data.data.id);
            if (!exists) {
              return [...prev, data.data];
            }
            return prev;
          });
          break;

        case "reaction_update":
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === data.data.id ? data.data : msg
            )
          );
          break;

        case "pong":
          break;

        default:
          console.log("Unknown message type:", data.type);
      }
    });

    const unsubscribeConnection = wsClient.onConnectionChange((connected) => {
      setIsConnected(connected);
      if (!connected) {
        setError("Disconnected from server. Attempting to reconnect...");
      } else {
        setError(null);
      }
    });

    return () => {
      unsubscribeMessages();
      unsubscribeConnection();
      wsClient.disconnect();
    };
  }, []);

  const handleSendMessage = async (newMessage) => {
    try {
      await postMessage(newMessage);
    } catch (err) {
      console.error("Failed to send", err);
      setError("Failed to send message");
    }
  };

  return {
    messages,
    setMessages,
    loading,
    error,
    isConnected,
    handleSendMessage,
  };
};
