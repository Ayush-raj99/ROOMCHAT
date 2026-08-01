"""
RoomChat V2

Room Routes
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.database import get_db
from app.models.models import User

from app.services.room_service import (
    create_room,
    get_room,
    user_can_access_room
)

from app.services.security import verify_password


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

templates = Jinja2Templates(
    directory="app/templates"
)


# =====================================================
# SCHEMAS
# =====================================================

class RoomCreate(BaseModel):
    name: str
    password: str


class RoomJoin(BaseModel):
    room_id: int
    username: str
    password: str


# =====================================================
# CREATE ROOM
# =====================================================

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
        "message": "Room created",
        "id": room.id,
        "name": room.name
    }


# =====================================================
# JOIN PAGE
# =====================================================

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

    if room is None:
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


# =====================================================
# JOIN ROOM
# =====================================================

@router.post("/join")
def join_room(
    data: RoomJoin,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    room = get_room(
        db,
        data.room_id
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    # ===============================
    # DEBUG
    # ===============================

    print("=" * 60)
    print("JOIN ROOM DEBUG")
    print("Username :", user.username)
    print("Password entered :", data.password)
    print("Hash in database :", room.password)

    result = verify_password(
        data.password,
        room.password
    )

    print("Password verified :", result)
    print("=" * 60)

    # ===============================

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Wrong room password"
        )

    if not user_can_access_room(
        db,
        user.id,
        room.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not assigned to this room."
        )

    return {
        "message": "Joined successfully",
        "room_id": room.id,
        "user_id": user.id,
        "username": user.username
    }