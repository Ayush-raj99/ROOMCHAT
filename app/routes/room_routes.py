"""
RoomChat V2

Room Routes

Handles:
- Room creation
- Join room page
- Room access verification
"""


from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db

from app.models.models import Room, User

from app.services.room_service import (
    create_room,
    get_room,
    user_can_access_room
)

from app.templates_engine import templates



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


    if not room:

        raise HTTPException(
            status_code=400,
            detail="Room creation failed"
        )


    return {

        "message": "Room created",

        "room_id": room.id,

        "room_name": room.name

    }



# ==========================================================
# JOIN ROOM PAGE
# ==========================================================


@router.api_route(
    "/join/{room_id}",
    methods=["GET", "HEAD"]
)
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
# JOIN ROOM VERIFY
# ==========================================================


@router.post("/join")
def join_room(
    data: RoomJoin,
    db: Session = Depends(get_db)
):


    user = db.query(User).filter(
        User.username == data.username
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    allowed = user_can_access_room(
        db,
        user.id,
        data.room_id
    )


    if not allowed:

        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )


    return {

        "message": "Room joined",

        "room_id": data.room_id

    }



# ==========================================================
# ROOM DETAILS
# ==========================================================


@router.get("/{room_id}")
def room_details(
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


    return {

        "id": room.id,

        "name": room.name

    }