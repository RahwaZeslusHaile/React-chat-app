import React, { useState, useEffect } from 'react';
import MessageReaction from './MessageReaction.jsx';
import ReplyList from './ReplyList.jsx';
import { postReply, fetchReplies } from '../utils/api.jsx';

function MessageItem({ message, onReactionChange }) {
    const [showReplyForm, setShowReplyForm] = useState(false);
    const [replyText, setReplyText] = useState('');
    const [replies, setReplies] = useState([]);
    const [loadingReplies, setLoadingReplies] = useState(false);
    const [submittingReply, setSubmittingReply] = useState(false);

    const isMe = message.username === "Rahwa";

    useEffect(() => {
        if (showReplyForm) {
            loadReplies();
        }
    }, [showReplyForm]);

    const loadReplies = async () => {
        setLoadingReplies(true);
        try {
            const fetchedReplies = await fetchReplies(message.id);
            setReplies(fetchedReplies);
        } catch (err) {
            console.error('Error loading replies:', err);
        } finally {
            setLoadingReplies(false);
        }
    };

    const handleReplySubmit = async (e) => {
        e.preventDefault();
        if (!replyText.trim()) return;

        setSubmittingReply(true);
        try {
            const newReply = await postReply(message.id, {
                username: "You",
                content: replyText
            });
            if (newReply) {
                setReplies([...replies, newReply]);
                setReplyText('');
            }
        } catch (err) {
            console.error('Error posting reply:', err);
        } finally {
            setSubmittingReply(false);
        }
    };

    const handleReplyReactionChange = (updatedReply) => {
        setReplies(replies.map(r => r.id === updatedReply.id ? updatedReply : r));
        if (onReactionChange) {
            onReactionChange(updatedReply);
        }
    };

    return (
        <div className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
            <div className="flex justify-between items-baseline text-sm text-gray-500">
                <span className={`font-semibold truncate ${isMe ? 'text-blue-600' : 'text-gray-700'}`}>
                    {message.username}
                </span>
                <span className="text-xs text-gray-400 flex-shrink-0 ml-2">
                    {message.timestamp}
                </span>
            </div>
            <div
                className={`px-3 py-2 rounded-2xl shadow-sm mt-1 break-words whitespace-normal
                            max-w-full sm:max-w-[70%]
                            ${isMe ? 'bg-blue-100' : 'bg-gray-100'}`}
                >
                {message.content}
            </div>

            <MessageReaction
                messageId={message.id}
                likes={message.likes}
                dislikes={message.dislikes}
                onReactionChange={onReactionChange}
            />

            <button
                onClick={() => setShowReplyForm(!showReplyForm)}
                className="text-xs text-blue-600 hover:text-blue-800 mt-2 font-medium"
            >
                {showReplyForm ? 'Hide Replies' : 'Reply'}
            </button>

            {showReplyForm && (
                <div className="w-full mt-3">
                    {loadingReplies ? (
                        <p className="text-xs text-gray-500">Loading replies...</p>
                    ) : (
                        <ReplyList replies={replies} onReactionChange={handleReplyReactionChange} />
                    )}

                    <form onSubmit={handleReplySubmit} className="mt-3">
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={replyText}
                                onChange={(e) => setReplyText(e.target.value)}
                                placeholder="Write a reply..."
                                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                disabled={submittingReply}
                            />
                            <button
                                type="submit"
                                disabled={submittingReply || !replyText.trim()}
                                className="px-3 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition"
                            >
                                {submittingReply ? 'Sending...' : 'Send'}
                            </button>
                        </div>
                    </form>
                </div>
            )}
        </div>
    );
}
export default MessageItem;