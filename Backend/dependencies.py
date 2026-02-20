from fastapi import Request,Depends;
from repository.repository_inmemory import InMemoryMessageRepository
from service.service import MessageService
from long_polling.poller import LongPoller
from websocket.connection_manager import ConnectionManager

def get_message_service(request: Request):
    return request.app.state.message_service

def get_poller(request: Request):
    return request.app.state.poller

def get_ws_manager(request: Request):
    return request.app.state.ws_manager