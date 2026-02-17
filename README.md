# FE Chat Application

A simple real-time chat application with a React frontend and a Python backend. Communication is implemented via REST endpoints and long-polling for near-real-time updates.

## Features

- Send and receive messages
- View messages from other users with timestamps
- Real-time updates via **WebSocket** or **Long-Polling**
- Message reactions (like / dislike) — stretch goal
- Reply, formatting, and color options — optional
- Automatic reconnection and connection status indicator

## Prerequisites

- Node.js (16+ recommended) and npm
- Python 3.8+ and virtualenv (for backend)

## Getting Started

1. Clone the repository

```bash
git clone <your-repo-url>
cd React-chat-app
```

2. Backend

```bash
cd Backend
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate  # Windows (PowerShell)
pip install -r requirements.txt
python app.py
```

3. Frontend

```bash
cd Frontend
npm install
npm run dev    
```

Open the frontend URL shown by the dev server (usually http://localhost:3000 or http://localhost:5173).

## Project Structure

- [Frontend](Frontend/) — React app
- [Backend](Backend/) — Python API server

## Tech Stack

- Frontend: React, WebSocket client
- Backend: Python (FastAPI), WebSocket support
- Communication: REST API + WebSocket (or Long-Polling as fallback)
- Optional: SQLAlchemy + SQLite for persistence

## Communication Options

### WebSocket (Recommended)
Real-time bidirectional communication with automatic reconnection. Configure via `VITE_USE_WEBSOCKET=true` environment variable.

### Long-Polling
Alternative polling mechanism for environments where WebSocket is not available. Configure via `VITE_USE_WEBSOCKET=false` environment variable.

For detailed WebSocket setup and deployment instructions, see [WEBSOCKET_README.md](WEBSOCKET_README.md).

## Development Notes

- The frontend and backend are separated into their respective folders for clarity.
- Use a virtual environment for backend development to isolate dependencies.
- The project follows a MoSCoW prioritization (MVP -> Stretch -> Optional) for features.
- Choose between WebSocket and Long-Polling based on your deployment environment.

## Contributing

PRs and issues are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License