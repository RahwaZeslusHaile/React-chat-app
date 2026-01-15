import ChatWindow from "./components/ChatWindow.jsx";
import React from "react";
import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([{id: 1, name: "Rahwa", text: "Hello!",timeStamp: "10:00"}, {id: 2, name: "Bob", text: "Hi there!",timeStamp: "10:01"}]);
  const handleSendMessage = (newMessage) => {
    setMessages([...messages, { ...newMessage, id: messages.length + 1 }]);
  };
  return (
    <div className="flex justify-center items-start min-h-screen bg-gray-100 p-6">
      <div className="w-full max-w-sm h-[700px] bg-white shadow-xl rounded-3xl flex flex-col overflow-hidden">
        <ChatWindow messages={messages} onSendMessage={handleSendMessage}>
        </ChatWindow>
      </div>
    </div>
  );
}

export default App;
