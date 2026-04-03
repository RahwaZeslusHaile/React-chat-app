
from fastapi import APIRouter,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from app.api.routes import messages,websocket,auth
from repository.repository_in_memory import InMemoryMessageRepository
from services.message_service import MessageService
from long_polling.poller import LongPoller
from websocket.connection_manager import ConnectionManager

logger = logging.getLogger(__name__)

async def scheduled_message_dispatcher(app: FastAPI):
    while True:
        await asyncio.sleep(5)
        try:
            service: MessageService = app.state.message_service
            ws_manager: ConnectionManager = app.state.ws_manager
            due_messages = service.get_due_scheduled_messages()
            for msg in due_messages:
                logger.info(f"Delivering scheduled message {msg.id}")
                if msg.parent_message_id:
                    await ws_manager.broadcast_new_reply(msg.to_dict(), msg.parent_message_id)
                else:
                    await ws_manager.broadcast_new_message(msg.to_dict())
        except Exception as e:
            logger.error(f"Error in scheduled message dispatcher: {e}")

@asynccontextmanager
async def lifespan(app:FastAPI):
    repository = InMemoryMessageRepository()
    app.state.message_service = MessageService(repository)
    app.state.poller = LongPoller(app.state.message_service)
    app.state.ws_manager = ConnectionManager()
    task = asyncio.create_task(scheduled_message_dispatcher(app))

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Chat API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "https://rahwafrontendchatapp.hosting.codeyourfuture.io",
            "https://frontendwschat.hosting.codeyourfuture.io",
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(messages.router)
app.include_router(websocket.router)
app.include_router(auth.router)

@app.get("/")
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "chat-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
