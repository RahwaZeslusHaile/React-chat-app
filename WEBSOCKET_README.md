# WebSocket Implementation

This branch adds WebSocket support to the chat application while keeping long-polling as an option.

## Features

- ✅ Real-time message updates via WebSocket
- ✅ Automatic reconnection on disconnect
- ✅ Fallback to long-polling (configurable)
- ✅ Connection status indicator
- ✅ Broadcast messages, replies, and reactions to all connected clients

## Architecture

### Backend
- **WebSocket endpoint**: `/ws`
- **Connection Manager**: Manages all active WebSocket connections
- **Broadcasting**: Automatically broadcasts new messages, replies, and reactions to all connected clients

### Frontend
- **WebSocket Client**: Singleton client with auto-reconnect
- **useWebSocket Hook**: React hook for WebSocket integration
- **Config-based switching**: Toggle between WebSocket and long-polling

## Setup

### 1. Install Backend Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### 2. Configure Frontend
Create a `.env.local` file in the Frontend directory:
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
# Enable WebSocket
VITE_USE_WEBSOCKET=true

# Production URLs
VITE_REST_URL=https://backendrahwachatapp.hosting.codeyourfuture.io
VITE_WS_URL=wss://backendwschat.hosting.codeyourfuture.io/ws

# Or for local development:
# VITE_REST_URL=http://localhost:8000
# VITE_WS_URL=ws://localhost:8000/ws
```

### 3. Run Locally

**Backend:**
```bash
cd Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd Frontend
npm install
npm run dev
```

## Deployment to Coolify

### Current Setup - Separate Deployments

You have separate deployments for different purposes:

1. **Long-Polling Backend**: `https://backendrahwachatapp.hosting.codeyourfuture.io`
   - Handles REST API endpoints
   - `/messages`, `/messages/longpoll`, etc.

2. **WebSocket Backend**: `https://backendwschat.hosting.codeyourfuture.io`
   - Handles WebSocket connections
   - `/ws` endpoint

3. **Frontend Deployments**:
   - Long-polling frontend: `https://rahwafrontendchatapp.hosting.codeyourfuture.io`
   - WebSocket frontend: `https://frontendwschat.hosting.codeyourfuture.io`

4. **Frontend Configuration** (for WebSocket deployment):
   ```env
   VITE_USE_WEBSOCKET=true
   VITE_REST_URL=https://backendrahwachatapp.hosting.codeyourfuture.io
   VITE_WS_URL=wss://backendwschat.hosting.codeyourfuture.io/ws
   ```

### Alternative - Single Deployment
You can also run both from a single backend deployment if preferred.

## Switching Between Long-Polling and WebSocket

### Via Environment Variable
Set `VITE_USE_WEBSOCKET=true` for WebSocket, `false` for long-polling.

### Programmatically
Edit [Frontend/src/config/api.js](Frontend/src/config/api.js):
```javascript
export const API_CONFIG = {
  USE_WEBSOCKET: true,  // Change this
  // ...
};
```

## Testing

### Test WebSocket Connection
```bash
# Install wscat
npm install -g wscat

# Connect to local server
wscat -c ws://localhost:8000/ws

# Connect to production
wscat -c wss://your-domain.com/ws

# Send ping
{"action": "ping"}

# Request messages
{"action": "get_messages"}
```

### Test Broadcasting
1. Open multiple browser tabs
2. Send a message from one tab
3. Verify all tabs receive the update instantly

## File Structure

```
Backend/
  main.py                          (WebSocket endpoint added)
  websocket/
    connection_manager.py          (Manages connections & broadcasting)
    handlers.py                    (WebSocket message handlers)

Frontend/
  src/
    config/
      api.js                       (API configuration)
    services/
      websocket/
        wsClient.js                (WebSocket client with reconnect)
  hooks/
    useWebSocket.js                (React hook for WebSocket)
    useMessagePolling.js           (Existing long-polling hook)
  .env.example                     (Environment variables template)
```

## Benefits Over Long-Polling

| Feature | Long-Polling | WebSocket |
|---------|-------------|-----------|
| Latency | ~2-30s | <100ms |
| Server Load | High (repeated requests) | Low (persistent connection) |
| Real-time | ❌ | ✅ |
| Connection Overhead | High | Low |
| Browser Support | Universal | Modern browsers |

## Troubleshooting

### WebSocket won't connect
- Check CORS settings in Backend/main.py
- Verify WebSocket URL (use `wss://` for HTTPS, `ws://` for HTTP)
- Check browser console for errors

### Messages not updating in real-time
- Verify `VITE_USE_WEBSOCKET=true`
- Check connection status indicator in UI
- Open browser DevTools > Network > WS tab

### Coolify deployment issues
- Ensure no firewall blocking WebSocket
- Check Coolify logs for connection errors
- Verify environment variables are set

## Next Steps

- [ ] Add authentication to WebSocket connections
- [ ] Implement typing indicators
- [ ] Add user presence (online/offline status)
- [ ] Implement private messaging
- [ ] Add message read receipts
