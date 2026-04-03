from fastapi import Request, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from repository.repository_in_memory import InMemoryMessageRepository
from services.message_service import MessageService
from long_polling.poller import LongPoller
from websocket.connection_manager import ConnectionManager
from app.core.jwt_handler import verify_token
from typing import Dict, Any

security = HTTPBearer()

def get_message_service(request: Request)->MessageService:
    return request.app.state.message_service

def get_poller(request: Request)->LongPoller:
    return request.app.state.poller

def get_ws_manager(request: Request)->ConnectionManager:
    return request.app.state.ws_manager

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:

    token = credentials.credentials
    payload = verify_token(token)
    return payload