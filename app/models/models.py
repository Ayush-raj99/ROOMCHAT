"""
RoomChat V2
Database Models

Tables:
- User
- Room
- Room Member
- Message
- Attachment
"""


from sqlalchemy import (

    Column,

    Integer,

    String,

    Text,

    Boolean,

    DateTime,

    ForeignKey

)

from sqlalchemy.orm import relationship

from datetime import datetime


from app.database.database import Base







# =====================================================
# USER TABLE
# =====================================================


class User(Base):


    __tablename__ = "users"



    id = Column(

        Integer,

        primary_key=True,

        index=True

    )



    username = Column(

        String(50),

        unique=True,

        nullable=False

    )



    display_name = Column(

        String(100),

        nullable=True

    )



    profile_picture = Column(

        String(255),

        nullable=True

    )



    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )




    messages = relationship(

        "Message",

        back_populates="user"

    )






# =====================================================
# ROOM TABLE
# =====================================================


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



    messages = relationship(

        "Message",

        back_populates="room"

    )






# =====================================================
# ROOM MEMBERS
# =====================================================


class RoomMember(Base):


    __tablename__ = "room_members"



    id = Column(

        Integer,

        primary_key=True

    )



    room_id = Column(

        Integer,

        ForeignKey(

            "rooms.id"

        )

    )



    user_id = Column(

        Integer,

        ForeignKey(

            "users.id"

        )

    )



    online = Column(

        Boolean,

        default=True

    )






# =====================================================
# MESSAGE TABLE
# =====================================================


class Message(Base):


    __tablename__ = "messages"



    id = Column(

        Integer,

        primary_key=True

    )



    room_id = Column(

        Integer,

        ForeignKey(

            "rooms.id"

        )

    )



    user_id = Column(

        Integer,

        ForeignKey(

            "users.id"

        )

    )



    content = Column(

        Text,

        nullable=False

    )



    message_type = Column(

        String(30),

        default="text"

    )



    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )



    seen = Column(

        Boolean,

        default=False

    )





    room = relationship(

        "Room",

        back_populates="messages"

    )



    user = relationship(

        "User",

        back_populates="messages"

    )








# =====================================================
# ATTACHMENT TABLE
# =====================================================


class Attachment(Base):


    __tablename__ = "attachments"



    id = Column(

        Integer,

        primary_key=True

    )



    message_id = Column(

        Integer,

        ForeignKey(

            "messages.id"

        )

    )



    file_url = Column(

        String(255)

    )



    file_type = Column(

        String(50)

    )



    uploaded_at = Column(

        DateTime,

        default=datetime.utcnow

    )