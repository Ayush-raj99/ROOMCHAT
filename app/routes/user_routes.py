"""
RoomChat V2
User Routes
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from app.database.database import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.services.user_service import (
    create_user,
    get_user,
    get_user_by_username,
    update_profile,
    set_online,
    set_offline
)





router = APIRouter(
    prefix="/users",
    tags=["Users"]
)





# ==========================================================
# CREATE USER
# ==========================================================

@router.post(
    "/",
    response_model=UserResponse
)
def create_new_user(

    data: UserCreate,

    db: Session = Depends(get_db)

):

    return create_user(

        db,

        data.username,

        data.display_name

    )





# ==========================================================
# GET USER
# ==========================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def read_user(

    user_id: int,

    db: Session = Depends(get_db)

):

    user = get_user(

        db,

        user_id

    )


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    return user





# ==========================================================
# GET USER BY USERNAME
# ==========================================================

@router.get(
    "/username/{username}",
    response_model=UserResponse
)
def read_user_by_username(

    username: str,

    db: Session = Depends(get_db)

):

    user = get_user_by_username(

        db,

        username

    )


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    return user





# ==========================================================
# UPDATE PROFILE
# ==========================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(

    user_id: int,

    data: UserUpdate,

    db: Session = Depends(get_db)

):

    user = update_profile(

        db,

        user_id,

        data.display_name,

        data.profile_picture

    )


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"

        )


    return user





# ==========================================================
# ONLINE
# ==========================================================

@router.post(
    "/{user_id}/online"
)
def user_online(

    user_id: int,

    db: Session = Depends(get_db)

):

    set_online(

        db,

        user_id

    )


    return {

        "status": "online"

    }





# ==========================================================
# OFFLINE
# ==========================================================

@router.post(
    "/{user_id}/offline"
)
def user_offline(

    user_id: int,

    db: Session = Depends(get_db)

):

    set_offline(

        db,

        user_id

    )


    return {

        "status": "offline"

    }