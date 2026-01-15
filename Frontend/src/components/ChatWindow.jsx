import React from "react";
import Header from "./Header.jsx";

function ChatWindow({children}){
    return(
        <div className="flex flex-col h-full">
            <Header />
            <div className="flex-1 overflow-y-auto p-4">
                {children} 
            </div>
        </div>  
    )
}
export default ChatWindow;