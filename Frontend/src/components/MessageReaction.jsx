import React from 'react';
import { addReaction } from '../utils/api.jsx';

export default function MessageReaction({ messageId, likes = 0, dislikes = 0, onReactionChange }) {
  const [loading, setLoading] = React.useState(false);
  const [localLikes, setLocalLikes] = React.useState(likes);
  const [localDislikes, setLocalDislikes] = React.useState(dislikes);

  const handleLike = async () => {
    setLoading(true);
    try {
      const updated = await addReaction(messageId, 'like');
      if (updated) {
        setLocalLikes(updated.likes);
        setLocalDislikes(updated.dislikes);
        if (onReactionChange) {
          onReactionChange(updated);
        }
      }
    } catch (err) {
      console.error('Error adding like:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDislike = async () => {
    setLoading(true);
    try {
      const updated = await addReaction(messageId, 'dislike');
      if (updated) {
        setLocalLikes(updated.likes);
        setLocalDislikes(updated.dislikes);
        if (onReactionChange) {
          onReactionChange(updated);
        }
      }
    } catch (err) {
      console.error('Error adding dislike:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-4 mt-2">
      <button
        onClick={handleLike}
        disabled={loading}
        className="flex items-center gap-1 px-3 py-1 rounded-full bg-green-100 hover:bg-green-200 text-green-700 text-sm font-medium disabled:opacity-50 transition"
      >
        👍 {localLikes}
      </button>
      <button
        onClick={handleDislike}
        disabled={loading}
        className="flex items-center gap-1 px-3 py-1 rounded-full bg-red-100 hover:bg-red-200 text-red-700 text-sm font-medium disabled:opacity-50 transition"
      >
        👎 {localDislikes}
      </button>
    </div>
  );
}
