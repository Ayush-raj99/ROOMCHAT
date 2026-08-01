"""
RoomChat V2

Admin Routes

Handles:
- Admin login page
- Admin authentication
- User management
- Room management
"""


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request


from fastapi.templating import Jinja2Templates


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






# ==================================================
# ROUTER
# ==================================================


router = APIRouter(

    prefix="/admin",

    tags=["Admin"]

)







templates = Jinja2Templates(

    directory="app/templates"

)







# ==================================================
# SCHEMAS
# ==================================================


class AdminLogin(BaseModel):

    username:str

    password:str






class CreateUser(BaseModel):

    username:str

    password:str






class CreateRoom(BaseModel):

    name:str

    password:str






class AssignRoom(BaseModel):

    user_id:int

    room_id:int






class ChangePassword(BaseModel):

    room_id:int

    password:str







# ==================================================
# ADMIN LOGIN PAGE
# ==================================================


@router.get("/login")

def admin_login_page(

    request:Request

):


    return templates.TemplateResponse(

        "admin_login.html",

        {

            "request":request

        }

    )







# ==================================================
# ADMIN LOGIN VERIFY
# ==================================================


@router.post("/login")

def admin_login(

    data:AdminLogin,

    db:Session = Depends(get_db)

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


        "message":"Login successful",


        "admin_id":admin.id


    }







# ==================================================
# ADMIN DASHBOARD PAGE
# ==================================================


@router.get("/dashboard")

def admin_dashboard(

    request:Request

):


    return templates.TemplateResponse(

        "admin_dashboard.html",

        {

            "request":request

        }

    )








# ==================================================
# CREATE USER
# ==================================================


@router.post("/users")

def add_user(

    data:CreateUser,

    db:Session = Depends(get_db)

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


        "message":"User created",

        "id":user.id

    }







# ==================================================
# GET USERS
# ==================================================


@router.get("/users")

def users(

    db:Session = Depends(get_db)

):


    return get_users(db)







# ==================================================
# CREATE ROOM
# ==================================================


@router.post("/rooms")

def add_room(

    data:CreateRoom,

    db:Session = Depends(get_db)

):


    room = create_room(

        db,

        data.name,

        data.password

    )



    return {


        "message":"Room created",

        "id":room.id

    }







# ==================================================
# GET ROOMS
# ==================================================


@router.get("/rooms")

def rooms(

    db:Session = Depends(get_db)

):


    return get_rooms(db)








# ==================================================
# ASSIGN USER TO ROOM
# ==================================================


@router.post("/assign")

def assign(

    data:AssignRoom,

    db:Session = Depends(get_db)

):


    result = assign_user_room(

        db,

        data.user_id,

        data.room_id

    )


    return {


        "message":"Assigned",

        "id":result.id

    }








# ==================================================
# CHANGE ROOM PASSWORD
# ==================================================


@router.put("/rooms/password")

def update_password(

    data:ChangePassword,

    db:Session = Depends(get_db)

):


    result = change_room_password(

        db,

        data.room_id,

        data.password

    )



    if not result:


        raise HTTPException(

            status_code=404,

            detail="Room not found"

        )



    return {


        "message":"Password changed"

    }








# ==================================================
# DELETE ROOM
# ==================================================


@router.delete("/rooms/{room_id}")

def remove_room(

    room_id:int,

    db:Session = Depends(get_db)

):


    result = delete_room(

        db,

        room_id

    )



    if not result:


        raise HTTPException(

            status_code=404,

            detail="Room not found"

        )



    return {


        "message":"Room deleted"

    }