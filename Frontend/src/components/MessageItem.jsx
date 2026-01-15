function MessageItem({ message }) {
    const isMe = message.name === "Rahwa";
    return (
        <div className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
            <div className="flex justify-between items-baseline text-sm text-gray-500">
                <span className={`font-semibold truncate ${isMe ? 'text-blue-600' : 'text-gray-700'}`}>
                    {message.name}
                </span>
                <span className="text-xs text-gray-400 flex-shrink-0 ml-2">
                    {message.timeStamp}
                </span>
            </div>
            <div className={`px-3 py-2 rounded-2xl max-w-[70%] break-words shadow-sm mt-1
                         ${isMe ? 'bg-blue-100' : 'bg-gray-100'}`}>
                {message.text}
            </div>
        </div>
    );
}
export default MessageItem;