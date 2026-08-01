"""
RoomChat V2
Admin Service

Handles:
- User management
- Room management
- Permissions
"""


from sqlalchemy.orm import Session

from app.models.models import User
from app.models.models import Room
from app.models.models import RoomMember

from app.services.security import hash_password



# ==========================================================
# CREATE USER
# ==========================================================

def create_user(

    db: Session,

    username: str,

    password: str

):


    existing = db.query(User).filter(

        User.username == username

    ).first()



    if existing:

        return None



    user = User(

        username=username,

        password=hash_password(password),

        role="user"

    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return user



# ==========================================================
# GET ALL USERS
# ==========================================================

def get_users(

    db: Session

):

    return db.query(User).filter(

        User.role == "user"

    ).all()



# ==========================================================
# GET ALL ROOMS
# ==========================================================

def get_rooms(

    db: Session

):

    return db.query(Room).all()



# ==========================================================
# DELETE ROOM
# ==========================================================

def delete_room(

    db: Session,

    room_id: int

):


    room = db.query(Room).filter(

        Room.id == room_id

    ).first()



    if not room:

        return False



    db.delete(room)

    db.commit()



    return True



# ==========================================================
# CHANGE ROOM PASSWORD
# ==========================================================

def change_room_password(

    db: Session,

    room_id: int,

    new_password: str

):


    room = db.query(Room).filter(

        Room.id == room_id

    ).first()



    if not room:

        return False



    room.password = hash_password(

        new_password

    )


    db.commit()



    return True



# ==========================================================
# ASSIGN USER TO ROOM
# ==========================================================

def assign_user_room(

    db: Session,

    user_id: int,

    room_id: int

):


    exists = db.query(RoomMember).filter(

        RoomMember.user_id == user_id,

        RoomMember.room_id == room_id

    ).first()



    if exists:

        return exists



    member = RoomMember(

        user_id=user_id,

        room_id=room_id

    )


    db.add(member)

    db.commit()

    db.refresh(member)


    return member



# ==========================================================
# REMOVE USER FROM ROOM
# ==========================================================

def remove_user_room(

    db: Session,

    user_id: int,

    room_id: int

):


    member = db.query(RoomMember).filter(

        RoomMember.user_id == user_id,

        RoomMember.room_id == room_id

    ).first()



    if not member:

        return False



    db.delete(member)

    db.commit()



    return True