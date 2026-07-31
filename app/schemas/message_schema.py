"""
RoomChat V2
Message Schemas
"""

from datetime import datetime

from pydantic import BaseModel





# ==========================================================
# CREATE MESSAGE
# ==========================================================

class MessageCreate(BaseModel):

    room_id: int

    user_id: int

    content: str | None = None





# ==========================================================
# EDIT MESSAGE
# ==========================================================

class MessageUpdate(BaseModel):

    content: str





# ==========================================================
# ATTACHMENT RESPONSE
# ==========================================================

class AttachmentResponse(BaseModel):

    id: int

    file_name: str

    file_url: str

    file_type: str

    file_size: int



    class Config:

        from_attributes = True





# ==========================================================
# MESSAGE RESPONSE
# ==========================================================

class MessageResponse(BaseModel):

    id: int

    room_id: int

    user_id: int

    content: str | None

    message_type: str

    delivered: bool

    seen: bool

    edited: bool

    deleted: bool

    created_at: datetime

    updated_at: datetime


    attachments: list[AttachmentResponse] = []



    class Config:

        from_attributes = True