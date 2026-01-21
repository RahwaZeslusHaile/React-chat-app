import React from "react";
import Header from "./Header.jsx";
import MessageList from "./MessageList.jsx";
import MessageInput from "./MessageInput.jsx";

function ChatWindow({ messages, onSendMessage , children }){ {
    return(
        <div className="flex flex-col h-full">
            <Header />
            <MessageList messages={messages} />
            <MessageInput onSend={onSendMessage} />
            <div className="flex-1 overflow-y-auto p-4">
                {children} 
            </div>
        </div>  
    )
}
}
export default ChatWindow;