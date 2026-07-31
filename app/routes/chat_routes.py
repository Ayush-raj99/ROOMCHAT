"""
RoomChat V2
Chat Routes

Handles:
- Opening chat room page
- Getting room messages
"""


from fastapi import (

    APIRouter,

    Depends,

    Request,

    HTTPException

)

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session



from app.database.database import get_db

from app.models.models import Room, Message



router = APIRouter(

    tags=["Chat"]

)



templates = Jinja2Templates(

    directory="app/templates"

)







# =====================================================
# OPEN CHAT ROOM
# =====================================================


@router.get("/chat/{room_id}")

def open_chat_room(

    request: Request,

    room_id: int,

    db: Session = Depends(get_db)

):


    room = db.query(Room).filter(

        Room.id == room_id

    ).first()





    if not room:


        raise HTTPException(

            status_code=404,

            detail="Room not found"

        )





    return templates.TemplateResponse(

        "chat.html",

        {

            "request": request,

            "room": room

        }

    )








# =====================================================
# GET ROOM MESSAGES
# =====================================================


@router.get("/chat/{room_id}/messages")

def get_room_messages(

    room_id: int,

    db: Session = Depends(get_db)

):


    messages = db.query(Message).filter(

        Message.room_id == room_id

    ).all()



    return messages