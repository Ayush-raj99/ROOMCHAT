"""
RoomChat V2
User Schemas
"""

from datetime import datetime

from pydantic import BaseModel





# ==========================================================
# CREATE USER
# ==========================================================

class UserCreate(BaseModel):

    username: str

    display_name: str | None = None





# ==========================================================
# UPDATE USER
# ==========================================================

class UserUpdate(BaseModel):

    display_name: str | None = None

    profile_picture: str | None = None





# ==========================================================
# USER RESPONSE
# ==========================================================

class UserResponse(BaseModel):

    id: int

    username: str

    display_name: str

    profile_picture: str

    is_online: bool

    last_seen: datetime

    created_at: datetime



    class Config:

        from_attributes = True