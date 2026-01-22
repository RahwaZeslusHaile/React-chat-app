const BASE_URL = "https://rahwachatapp.hosting.codeyourfuture.io";

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
