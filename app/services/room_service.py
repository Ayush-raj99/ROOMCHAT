"""
RoomChat V2
Room Service
"""

from sqlalchemy.orm import Session

from app.models.models import Room

from app.services.security import (
    hash_password,
    verify_password
)



# ==========================================
# CREATE ROOM
# ==========================================

def create_room(

    db: Session,

    name: str,

    password: str

):

    room = Room(

        name=name,

        password=hash_password(password)

    )

    db.add(room)

    db.commit()

    db.refresh(room)

    return room



# ==========================================
# GET ALL ROOMS
# ==========================================

def get_all_rooms(

    db: Session

):

    return (

        db.query(Room)

        .order_by(Room.id)

        .all()

    )



# ==========================================
# GET ROOM BY ID
# ==========================================

def get_room(

    db: Session,

    room_id: int

):

    return (

        db.query(Room)

        .filter(Room.id == room_id)

        .first()

    )



# ==========================================
# GET ROOM BY NAME
# ==========================================

def get_room_by_name(

    db: Session,

    name: str

):

    return (

        db.query(Room)

        .filter(Room.name == name)

        .first()

    )



# ==========================================
# VERIFY ROOM PASSWORD
# ==========================================

def verify_room_password(

    db: Session,

    room_id: int,

    password: str

):

    room = get_room(

        db,

        room_id

    )

    if room is None:

        return False

    return verify_password(

        password,

        room.password

    )



# ==========================================
# DELETE ROOM
# ==========================================

def delete_room(

    db: Session,

    room_id: int

):

    room = get_room(

        db,

        room_id

    )

    if room is None:

        return False

    db.delete(room)

    db.commit()

    return True