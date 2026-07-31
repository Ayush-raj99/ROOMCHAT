"""
RoomChat V2
Room Routes

Handles:
- Create room
- Get rooms
- Join room
"""


from fastapi import (

    APIRouter,

    Depends,

    HTTPException

)

from sqlalchemy.orm import Session



from app.database.database import get_db


from app.models.models import Room


from app.schemas.room_schema import (

    RoomCreate,

    RoomResponse,

    RoomJoin

)


from app.services.room_service import (

    create_room,

    get_all_rooms

)





router = APIRouter(

    prefix="/rooms",

    tags=["Rooms"]

)







# ==========================================================
# CREATE ROOM
# ==========================================================


@router.post(

    "/",

    response_model=RoomResponse

)

def create_new_room(

    data: RoomCreate,

    db: Session = Depends(get_db)

):


    room = create_room(

        db,

        data.name,

        data.password

    )


    return room







# ==========================================================
# GET ALL ROOMS
# ==========================================================


@router.get(

    "/",

    response_model=list[RoomResponse]

)

def list_rooms(

    db: Session = Depends(get_db)

):


    return get_all_rooms(

        db

    )







# ==========================================================
# JOIN ROOM
# ==========================================================


@router.post(

    "/join"

)

def join_room(

    data: RoomJoin,

    db: Session = Depends(get_db)

):


    room = db.query(Room).filter(

        Room.id == data.room_id

    ).first()





    if not room:


        raise HTTPException(

            status_code=404,

            detail="Room not found"

        )







    if room.password != data.password:


        raise HTTPException(

            status_code=401,

            detail="Wrong password"

        )






    return {


        "message":

        "Joined successfully",


        "room_id":

        room.id,


        "room_name":

        room.name,


        "username":

        data.username


    }