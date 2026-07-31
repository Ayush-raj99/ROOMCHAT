"""
RoomChat V2
User Service

Handles:
- Create users
- Find users
- Update profile
- Online status
- User management
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.models import User





# ==========================================================
# CREATE USER
# ==========================================================

def create_user(

    db: Session,

    username: str,

    display_name: str = None

):

    existing_user = (

        db.query(User)

        .filter(

            User.username == username

        )

        .first()

    )


    if existing_user:

        return existing_user



    user = User(

        username=username,

        display_name=display_name or username

    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return user





# ==========================================================
# GET USER BY ID
# ==========================================================

def get_user(

    db: Session,

    user_id: int

):

    return (

        db.query(User)

        .filter(

            User.id == user_id

        )

        .first()

    )





# ==========================================================
# GET USER BY USERNAME
# ==========================================================

def get_user_by_username(

    db: Session,

    username: str

):

    return (

        db.query(User)

        .filter(

            User.username == username

        )

        .first()

    )





# ==========================================================
# UPDATE PROFILE
# ==========================================================

def update_profile(

    db: Session,

    user_id: int,

    display_name: str = None,

    profile_picture: str = None

):

    user = get_user(

        db,

        user_id

    )


    if not user:

        return None



    if display_name:

        user.display_name = display_name



    if profile_picture:

        user.profile_picture = profile_picture



    user.updated_at = datetime.utcnow()



    db.commit()

    db.refresh(user)


    return user





# ==========================================================
# SET ONLINE
# ==========================================================

def set_online(

    db: Session,

    user_id: int

):

    user = get_user(

        db,

        user_id

    )


    if user:

        user.is_online = True

        user.last_seen = datetime.utcnow()

        db.commit()



    return user





# ==========================================================
# SET OFFLINE
# ==========================================================

def set_offline(

    db: Session,

    user_id: int

):

    user = get_user(

        db,

        user_id

    )


    if user:

        user.is_online = False

        user.last_seen = datetime.utcnow()

        db.commit()



    return user





# ==========================================================
# DELETE USER
# ==========================================================

def delete_user(

    db: Session,

    user_id: int

):

    user = get_user(

        db,

        user_id

    )


    if not user:

        return False



    db.delete(user)

    db.commit()


    return True