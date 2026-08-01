"""
RoomChat V2
Chat Routes

Handles:
- Chat page
- Message history
"""


from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import HTTPException

from app.templates_engine import templates

from sqlalchemy.orm import Session


from app.database.database import get_db


from app.services.room_service import get_room

from app.services.chat_service import get_room_messages



# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(

    prefix="/chat",

    tags=["Chat"]

)



# ==========================================================
# TEMPLATE
# ========================================================


# ==========================================================
# OPEN CHAT ROOM
# ==========================================================

@router.get("/{room_id}")

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

        "chat.html",

        {

            "request":request,

            "room":room

        }

    )



# ==========================================================
# GET OLD MESSAGES
# ==========================================================

@router.get("/{room_id}/messages")

def messages(

    room_id:int,

    db:Session = Depends(get_db)

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