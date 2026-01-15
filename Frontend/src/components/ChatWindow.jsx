import React from "react";
import Header from "./Header.jsx";
import MessageList from "./MessageList.jsx";
import MessageInput from "./MessageInput.jsx";

function ChatWindow({children, messages}) {
    return(
        <div className="flex flex-col h-full">
            <Header />
            <MessageList messages={messages} />
            <MessageInput onSend={(data)=>console.log(data)} />
            <div className="flex-1 overflow-y-auto p-4">
                {children} 
            </div>
        </div>  
    )
}
export default ChatWindow;