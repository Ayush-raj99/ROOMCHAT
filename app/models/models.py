"""
RoomChat V2
Database Models

Contains:
- Users
- Rooms
- Room Members
- Messages
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from app.database.database import Base


# ==========================================================
# USERS TABLE
# ==========================================================

class User(Base):

    __tablename__ = "users"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    username = Column(

        String(100),

        unique=True,

        nullable=False

    )


    password = Column(

        String(255),

        nullable=False

    )


    role = Column(

        String(20),

        default="user"

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


    rooms = relationship(

        "RoomMember",

        back_populates="user",

        cascade="all, delete"

    )


    messages = relationship(

        "Message",

        back_populates="user"

    )



# ==========================================================
# ROOMS TABLE
# ==========================================================

class Room(Base):

    __tablename__ = "rooms"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    name = Column(

        String(100),

        nullable=False

    )


    password = Column(

        String(255),

        nullable=False

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


    members = relationship(

        "RoomMember",

        back_populates="room",

        cascade="all, delete"

    )


    messages = relationship(

        "Message",

        back_populates="room",

        cascade="all, delete"

    )



# ==========================================================
# ROOM MEMBERS TABLE
# Controls who can enter which room
# ==========================================================

class RoomMember(Base):

    __tablename__ = "room_members"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    room_id = Column(

        Integer,

        ForeignKey("rooms.id"),

        nullable=False

    )


    user_id = Column(

        Integer,

        ForeignKey("users.id"),

        nullable=False

    )


    room = relationship(

        "Room",

        back_populates="members"

    )


    user = relationship(

        "User",

        back_populates="rooms"

    )



# ==========================================================
# MESSAGES TABLE
# Supports text + file uploads
# ==========================================================

class Message(Base):

    __tablename__ = "messages"


    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    room_id = Column(

        Integer,

        ForeignKey("rooms.id"),

        nullable=False

    )


    user_id = Column(

        Integer,

        ForeignKey("users.id"),

        nullable=False

    )


    content = Column(

        Text,

        nullable=True

    )


    file_name = Column(

        String(255),

        nullable=True

    )


    file_path = Column(

        String(500),

        nullable=True

    )


    is_image = Column(

        Boolean,

        default=False

    )


    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


    room = relationship(

        "Room",

        back_populates="messages"

    )


    user = relationship(

        "User",

        back_populates="messages"

    )