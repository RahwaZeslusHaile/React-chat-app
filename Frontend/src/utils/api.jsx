import { API_CONFIG } from "../config/api.js";

const BASE_URL = API_CONFIG.REST_URL;

export const fetchMessages = async () => {
  try {
    const res = await fetch(`${BASE_URL}/messages`);
    if (!res.ok) {
      console.error("Failed to fetch messages:", res.status, res.statusText);
      return []; 
    }
    const data = await res.json();
    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error("Error fetching messages:", err);
    return [];
  }
};

export const postMessage = async (message) => {
  try {
    const res = await fetch(`${BASE_URL}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(message),
    });
    if (!res.ok) {
      console.error("Failed to post message:", res.status, res.statusText);
      return null;
    }
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Error posting message:", err);
    return null;
  }
};

export const pollMessages = async (afterTimestamp) => {
  try {
    const res = await fetch(`${BASE_URL}/messages/longpoll?after=${encodeURIComponent(afterTimestamp)}`);
    if (!res.ok) {
      console.error("Failed to poll messages:", res.status, res.statusText);
      return [];
    }
    const data = await res.json();
    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error("Error polling messages:", err);
    return [];
  }
};

export const postReply = async (messageId, reply) => {
  try {
    const res = await fetch(`${BASE_URL}/messages/${messageId}/replies`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reply),
    });
    if (!res.ok) {
      console.error("Failed to post reply:", res.status, res.statusText);
      return null;
    }
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Error posting reply:", err);
    return null;
  }
};

export const fetchReplies = async (messageId) => {
  try {
    const res = await fetch(`${BASE_URL}/messages/${messageId}/replies`);
    if (!res.ok) {
      console.error("Failed to fetch replies:", res.status, res.statusText);
      return [];
    }
    const data = await res.json();
    return Array.isArray(data) ? data : [];
  } catch (err) {
    console.error("Error fetching replies:", err);
    return [];
  }
};

export const addReaction = async (messageId, reactionType) => {
  try {
    const res = await fetch(`${BASE_URL}/messages/${messageId}/reactions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reaction_type: reactionType }),
    });
    if (!res.ok) {
      console.error("Failed to add reaction:", res.status, res.statusText);
      return null;
    }
    const data = await res.json();
    return data;
  } catch (err) {
    console.error("Error adding reaction:", err);
    return null;
  }
};
