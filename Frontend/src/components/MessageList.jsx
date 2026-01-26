import { useEffect, useRef } from "react";
import MessageItem from "./MessageItem.jsx";

function MessageList({ messages, onReactionChange }) {
  const messageEndRef = useRef(null);

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (!Array.isArray(messages)) return null;

  const topLevelMessages = messages.filter(msg => !msg.parent_message_id);

  return (
    <div className="flex flex-col p-4 space-y-4 overflow-y-auto h-full">
      {topLevelMessages.map((msg) => (
        <MessageItem
          key={msg.id}
          message={msg}
          onReactionChange={onReactionChange}
        />
      ))}
      <div ref={messageEndRef} />
    </div>
  );
}

export default MessageList;
