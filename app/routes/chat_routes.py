"""
RoomChat V2

Chat Routes

Handles:
- Chat page
- Message history
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.room_service import get_room
from app.services.chat_service import get_room_messages


# ==================================================
# ROUTER
# ==================================================

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# ==================================================
# TEMPLATE
# ==================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ==================================================
# OPEN CHAT ROOM
# ==================================================

@router.api_route(
    "/{room_id}",
    methods=["GET", "HEAD"]
)
def open_chat(
    request: Request,
    room_id: int,
    db: Session = Depends(get_db)
):

    room = get_room(
        db,
        room_id
    )

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "room": room
        }
    )


# ==================================================
# GET OLD MESSAGES
# ==================================================

@router.get("/{room_id}/messages")
def messages(
    room_id: int,
    db: Session = Depends(get_db)
):

    room = get_room(
        db,
        room_id
    )

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return get_room_messages(
        db,
        room_id
    )