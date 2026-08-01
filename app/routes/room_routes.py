"""
RoomChat V2
Room Routes

Handles:
- Room creation
- Join room page
- Room access verification
"""


from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import HTTPException

from app.templates_engine import templates

from sqlalchemy.orm import Session

from pydantic import BaseModel


from app.database.database import get_db


from app.models.models import User
from app.models.models import Room


from app.services.security import verify_password


from app.services.room_service import (
    create_room,
    get_room,
    user_can_access_room
)



# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(

    prefix="/rooms",

    tags=["Rooms"]

)




# ==========================================================
# SCHEMAS
# ==========================================================

class RoomCreate(BaseModel):

    name: str

    password: str



class RoomJoin(BaseModel):

    room_id: int

    username: str

    password: str



# ==========================================================
# CREATE ROOM
# ==========================================================

@router.post("/")

def create_new_room(

    data: RoomCreate,

    db: Session = Depends(get_db)

):


    room = create_room(

        db,

        data.name,

        data.password

    )


    return {

        "id": room.id,

        "name": room.name

    }



# ==========================================================
# JOIN PAGE
# ==========================================================

@router.get("/join/{room_id}")

def join_room_page(

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

        "join_room.html",

        {

            "request": request,

            "room": room

        }

    )



# ==========================================================
# VERIFY JOIN
# ==========================================================

@router.post("/join")

def join_room(

    data: RoomJoin,

    db: Session = Depends(get_db)

):


    room = get_room(

        db,

        data.room_id

    )


    if not room:

        raise HTTPException(

            status_code=404,

            detail="Room not found"

        )



    # Check room password

    if not verify_password(

        data.password,

        room.password

    ):

        raise HTTPException(

            status_code=401,

            detail="Wrong room password"

        )



    # Find user

    user = db.query(User).filter(

        User.username == data.username

    ).first()



    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )



    # Check permission

    if not user_can_access_room(

        db,

        user.id,

        room.id

    ):

        raise HTTPException(

            status_code=403,

            detail="You are not allowed in this room"

        )



    return {


        "message":"Joined successfully",


        "user_id":user.id,


        "username":user.username,


        "room_id":room.id

    }