"""
RoomChat V2

Admin Routes

Handles:
- Admin login
- Admin dashboard
- User management
- Room management
"""


from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel


from app.database.database import get_db

from app.models.models import User

from app.services.security import verify_password

from app.services.admin_service import (
    create_user,
    get_users,
    get_rooms,
    delete_room,
    change_room_password,
    assign_user_room
)

from app.services.room_service import create_room

from app.templates_engine import templates



# ==========================================================
# ROUTER
# ==========================================================


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)



# ==========================================================
# SCHEMAS
# ==========================================================


class AdminLogin(BaseModel):

    username: str

    password: str



class CreateUserSchema(BaseModel):

    username: str

    password: str



class CreateRoomSchema(BaseModel):

    name: str

    password: str



class AssignRoomSchema(BaseModel):

    user_id: int

    room_id: int



class ChangePasswordSchema(BaseModel):

    room_id: int

    password: str



# ==========================================================
# ADMIN LOGIN PAGE
# ==========================================================


@router.api_route(
    "/login",
    methods=["GET", "HEAD"]
)
def admin_login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={}
    )



# ==========================================================
# ADMIN LOGIN VERIFY
# ==========================================================


@router.post("/login")
def admin_login(
    data: AdminLogin,
    db: Session = Depends(get_db)
):

    admin = db.query(User).filter(
        User.username == data.username,
        User.role == "admin"
    ).first()



    if not admin:

        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )



    if not verify_password(
        data.password,
        admin.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )



    return {

        "message": "Login successful",

        "admin_id": admin.id

    }



# ==========================================================
# ADMIN DASHBOARD
# ==========================================================


@router.api_route(
    "/dashboard",
    methods=["GET", "HEAD"]
)
def admin_dashboard(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={}
    )



# ==========================================================
# CREATE USER
# ==========================================================


@router.post("/users")
def add_user(
    data: CreateUserSchema,
    db: Session = Depends(get_db)
):

    user = create_user(
        db,
        data.username,
        data.password
    )


    if not user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    return {

        "message": "User created",

        "id": user.id

    }



# ==========================================================
# GET USERS
# ==========================================================


@router.get("/users")
def users(
    db: Session = Depends(get_db)
):

    return get_users(db)



# ==========================================================
# CREATE ROOM
# ==========================================================


@router.post("/rooms")
def add_room(
    data: CreateRoomSchema,
    db: Session = Depends(get_db)
):

    room = create_room(
        db,
        data.name,
        data.password
    )


    return {

        "message": "Room created",

        "room_id": room.id

    }



# ==========================================================
# GET ROOMS
# ==========================================================


@router.get("/rooms")
def rooms(
    db: Session = Depends(get_db)
):

    return get_rooms(db)



# ==========================================================
# DELETE ROOM
# ==========================================================


@router.delete("/rooms/{room_id}")
def remove_room(
    room_id: int,
    db: Session = Depends(get_db)
):

    result = delete_room(
        db,
        room_id
    )


    return {

        "message": "Room deleted",

        "result": result

    }



# ==========================================================
# CHANGE ROOM PASSWORD
# ==========================================================


@router.post("/rooms/password")
def update_room_password(
    data: ChangePasswordSchema,
    db: Session = Depends(get_db)
):

    result = change_room_password(
        db,
        data.room_id,
        data.password
    )


    return {

        "message": "Password changed",

        "result": result

    }



# ==========================================================
# ASSIGN USER TO ROOM
# ==========================================================


@router.post("/assign-room")
def assign_room(
    data: AssignRoomSchema,
    db: Session = Depends(get_db)
):

    result = assign_user_room(
        db,
        data.user_id,
        data.room_id
    )


    return {

        "message": "User assigned",

        "result": result


    }
@router.get("/debug-members")
def debug_members(
    db: Session = Depends(get_db)
):

    from app.models.models import RoomMember

    members = db.query(RoomMember).all()

    return [
        {
            "id": m.id,
            "user_id": m.user_id,
            "room_id": m.room_id
        }
        for m in members
    ]
