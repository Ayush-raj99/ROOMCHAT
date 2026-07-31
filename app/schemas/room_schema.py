"""
RoomChat V2
Room Schemas
"""

from datetime import datetime

from pydantic import BaseModel





# ==========================================================
# CREATE ROOM
# ==========================================================

class RoomCreate(BaseModel):

    name: str

    password: str





# ==========================================================
# JOIN ROOM
# ==========================================================

class RoomJoin(BaseModel):

    room_id: int

    password: str

    username: str





# ==========================================================
# ROOM RESPONSE
# ==========================================================

class RoomResponse(BaseModel):

    id: int

    name: str

    created_at: datetime



    class Config:

        from_attributes = True


class RoomJoin(BaseModel):

    room_id: int

    password: str

    username: str