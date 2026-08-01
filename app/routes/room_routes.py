"""
RoomChat V2

Room Routes

Handles:
- Create room
- Join room page
- Room access verification
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db

from app.services.room_service import (
    create_room,
    get_room,
    user_can_access_room
)


# ==================================================
# ROUTER
# ==================================================

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


# ==================================================
# TEMPLATE ENGINE
# ==================================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ==================================================
# SCHEMAS
# ==================================================

class RoomCreate(BaseModel):
    name: str
    password: str


class RoomJoin(BaseModel):
    room_id: int
    username: str
    password: str


# ==================================================
# CREATE ROOM
# ==================================================

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
            detail="Room already exists"
        )

    return {
        "message": "Room created",
        "id": room.id,
        "name": room.name
    }


# ==================================================
# JOIN ROOM PAGE
# ==================================================

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
        request=request,
        name="join_room.html",
        context={
            "room": room
        }
    )


# ==================================================
# JOIN ROOM VERIFY
# ==================================================

@router.post("/join")
def join_room(
    data: RoomJoin,
    db: Session = Depends(get_db)
):

    allowed = user_can_access_room(
        db,
        data.username,
        data.room_id,
        data.password
    )

    if not allowed:
        raise HTTPException(
            status_code=401,
            detail="Invalid room password or access denied"
        )

    return {
        "message": "Joined room successfully",
        "room_id": data.room_id,
        "username": data.username
    }