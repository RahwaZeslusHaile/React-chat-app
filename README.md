# FE Chat Application

A simple real-time chat application with a React frontend and a Python backend. Communication is implemented via REST endpoints and long-polling for near-real-time updates.

## Features

- Send and receive messages
- View messages from other users with timestamps
- Long-polling message fetch
- Message reactions (like / dislike) — stretch goal
- Reply, formatting, and color options — optional

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
# Start the backend (example)
python app.py
```

3. Frontend

```bash
cd Frontend
npm install
npm run dev    # or `npm start` depending on the project scripts
```

Open the frontend URL shown by the dev server (usually http://localhost:3000 or http://localhost:5173).

## Project Structure

- [Frontend](Frontend/) — React app
- [Backend](Backend/) — Python API server

## Tech Stack

- Frontend: React, Axios (HTTP)
- Backend: Python (Flask or FastAPI), optional SQLAlchemy + SQLite
- Communication: REST API + Long-Polling

## Development Notes

- The frontend and backend are separated into their respective folders for clarity.
- Use a virtual environment for backend development to isolate dependencies.
- The project follows a MoSCoW prioritization (MVP -> Stretch -> Optional) for features.

## Contributing

PRs and issues are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License