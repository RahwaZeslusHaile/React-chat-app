from datetime import datetime, timezone
from fastapi import APIRouter,HTTPException,Query,Depends
from typing import Optional,List,Dict,Any


from core.dependencies import get_message_service,get_poller,get_ws_manager,get_current_user
from services.message_service import MessageService
from long_polling.poller import LongPoller
from schemas.message import(MessageRequest,MessageResponse,ReplyRequest)
from schemas.reaction import ReactionRequest
from websocket.connection_manager import ConnectionManager

router = APIRouter(prefix="/messages", tags=["messages"])

def parse_iso_datetime(value:str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z","+00:00"))
    if parsed.tzinfo is not None:
       return parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed

@router.get("",response_model=List[MessageResponse])
def get_messages(
    after:Optional[str] = Query(None),
    message_service: MessageService =Depends(get_message_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        if after:
            after_dt = parse_iso_datetime(after)
            messages = message_service.get_messages_after(after_dt)
        else:
            messages = message_service.get_all_messages()

        return[MessageResponse(**msg.to_dict()) for msg in messages]
        
    except ValueError:
        raise HTTPException(status_code = 400, detail = "Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code = 500, detail = "Internal server error")
    

@router.get("/longpoll",response_model=List[MessageResponse])
def long_poll_message(
    after: str = Query(...),
    poller: LongPoller = Depends(get_poller),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        after_dt = parse_iso_datetime(after)
        new_messages = poller.wait_for_new_messages(after_dt)

        sorted_messages = sorted(
            new_messages,
            key=lambda m:m.timestamp.value,
            reverse=True,
        )
        return [MessageResponse(**m.to_dict()) for m in sorted_messages]
    
    except ValueError:
        raise HTTPException(status_code=400 , detail= "Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail = "Internal server error")
    

@router.get("/{message_id}",response_model=MessageResponse)
def get_message_by_ID(
    message_id:str,
    message_service:MessageService = Depends(get_message_service),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        message = message_service.get_message_by_id(message_id)
     
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        return MessageResponse(**message.to_dict())

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("", response_model=MessageResponse)
async def create_message(
    request: MessageRequest,
    message_service: MessageService = Depends(get_message_service),
    ws_manager: ConnectionManager = Depends(get_ws_manager),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        scheduled_dt = (
            parse_iso_datetime(request.scheduled_for)
            if request.scheduled_for
            else None
        )

        message = message_service.create_message(
            username=request.username,
            content=request.content,
            scheduled_for=scheduled_dt,
            text_color=request.text_color,
            is_bold=request.is_bold,
            is_italic=request.is_italic,
        )

        if not scheduled_dt or scheduled_dt <= datetime.now():
            await ws_manager.broadcast_new_message(message.to_dict())

        return MessageResponse(**message.to_dict())

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{message_id}/replies", response_model=MessageResponse)
async def create_reply(
    message_id: str,
    request: ReplyRequest,
    message_service: MessageService = Depends(get_message_service),
    ws_manager: ConnectionManager = Depends(get_ws_manager),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        scheduled_dt = (
            parse_iso_datetime(request.scheduled_for)
            if request.scheduled_for
            else None
        )

        reply = message_service.create_reply(
            username=request.username,
            content=request.content,
            parent_message_id=message_id,
            scheduled_for=scheduled_dt,
            text_color=request.text_color,
            is_bold=request.is_bold,
            is_italic=request.is_italic,
        )

        if not scheduled_dt or scheduled_dt <= datetime.now():
            await ws_manager.broadcast_new_reply(reply.to_dict(), message_id)

        return MessageResponse(**reply.to_dict())

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{message_id}/replies", response_model=List[MessageResponse])
def get_replies(
    message_id: str,
    message_service: MessageService = Depends(get_message_service),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        message = message_service.get_message_by_id(message_id)

        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        replies = message_service.get_replies(message_id)

        return [MessageResponse(**reply.to_dict()) for reply in replies]

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{message_id}/reactions", response_model=MessageResponse)
async def add_reaction(
    message_id: str,
    request: ReactionRequest,
    message_service: MessageService = Depends(get_message_service),
    ws_manager: ConnectionManager = Depends(get_ws_manager),
    current_user: Dict[str, Any] = Depends(get_current_user),
):
    try:
        message = message_service.add_reaction(
            message_id,
            request.reaction_type,
        )

        await ws_manager.broadcast_reaction(message.to_dict())

        return MessageResponse(**message.to_dict())

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid reaction type")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")