import { useEffect,useRef } from "react";

function MessageList({ messages }) {
    const messageEndRef = useRef(null);

    useEffect(() => {
        messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);
    return (
        <div className="flex flex-col p-4 space-y-4 overflow-y-auto h-full">
            {messages.map((msg) => (
                <div key={msg.id} className="flex flex-col">
                    <div className="flex justify-between items-baseline text-sm text-gray-500">
                        <span className="font-semibold text-gray-700 truncate">
                            {msg.name}
                        </span>
                        <span className="text-xs text-gray-400 flex-shrink-0">
                            {msg.timeStamp}
                        </span>
                    </div>
                    <div className="bg-blue-100 p-3 rounded-2xl max-w-xs break-words shadow-sm mt-1">
                        {msg.text}
                    </div>
                </div>
            ))}
        </div>
    );
}

export default MessageList;
