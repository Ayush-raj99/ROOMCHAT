"""
RoomChat V2
Room Service

Handles:
- Room creation
- Room listing
- Room access
- User-room assignment
"""

from sqlalchemy.orm import Session

from app.models.models import Room
from app.models.models import RoomMember
from app.models.models import User

from app.services.security import hash_password



# ==========================================================
# CREATE ROOM
# ==========================================================

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



# ==========================================================
# GET ALL ROOMS
# ==========================================================

def get_all_rooms(

    db: Session

):

    return db.query(Room).all()



# ==========================================================
# GET ROOM BY ID
# ==========================================================

def get_room(

    db: Session,

    room_id: int

):

    return db.query(Room).filter(

        Room.id == room_id

    ).first()



# ==========================================================
# ADD USER TO ROOM
# ==========================================================

def add_user_to_room(

    db: Session,

    user_id: int,

    room_id: int

):


    existing = db.query(RoomMember).filter(

        RoomMember.user_id == user_id,

        RoomMember.room_id == room_id

    ).first()



    if existing:

        return existing



    member = RoomMember(

        user_id=user_id,

        room_id=room_id

    )


    db.add(member)

    db.commit()

    db.refresh(member)


    return member



# ==========================================================
# CHECK USER ROOM ACCESS
# ==========================================================

def user_can_access_room(

    db: Session,

    user_id: int,

    room_id: int

):


    user = db.query(User).filter(

        User.id == user_id

    ).first()



    if not user:

        return False



    # Admin can access every room

    if user.role == "admin":

        return True



    member = db.query(RoomMember).filter(

        RoomMember.user_id == user_id,

        RoomMember.room_id == room_id

    ).first()



    if member:

        return True



    return False
    