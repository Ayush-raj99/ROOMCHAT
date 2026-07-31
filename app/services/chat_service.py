"""
RoomChat V2
Chat Service

Handles:
- Create messages
- Get chat history
- Edit messages
- Delete messages
- Delivery status
- Seen status
"""

from sqlalchemy.orm import Session

from app.models.models import (
    Message,
    User,
    Room,
    Attachment
)





# ==========================================================
# CREATE MESSAGE
# ==========================================================

def create_message(

    db: Session,

    room_id: int,

    user_id: int,

    content: str = None,

    message_type: str = "text"

):

    message = Message(

        room_id=room_id,

        user_id=user_id,

        content=content,

        message_type=message_type

    )


    db.add(message)

    db.commit()

    db.refresh(message)


    return message





# ==========================================================
# GET ROOM MESSAGES
# ==========================================================

def get_room_messages(

    db: Session,

    room_id: int,

    limit: int = 50

):

    return (

        db.query(Message)

        .filter(

            Message.room_id == room_id,

            Message.deleted == False

        )

        .order_by(

            Message.created_at.desc()

        )

        .limit(limit)

        .all()

    )





# ==========================================================
# GET SINGLE MESSAGE
# ==========================================================

def get_message(

    db: Session,

    message_id: int

):

    return (

        db.query(Message)

        .filter(

            Message.id == message_id

        )

        .first()

    )





# ==========================================================
# EDIT MESSAGE
# ==========================================================

def edit_message(

    db: Session,

    message_id: int,

    new_content: str

):

    message = get_message(

        db,

        message_id

    )


    if not message:

        return None



    message.content = new_content

    message.edited = True


    db.commit()

    db.refresh(message)


    return message





# ==========================================================
# DELETE MESSAGE
# ==========================================================

def delete_message(

    db: Session,

    message_id: int

):

    message = get_message(

        db,

        message_id

    )


    if not message:

        return False



    message.deleted = True


    db.commit()


    return True
    # ==========================================================
# MARK MESSAGE DELIVERED
# ==========================================================

def mark_delivered(

    db: Session,

    message_id: int

):

    message = get_message(

        db,

        message_id

    )


    if not message:

        return None



    message.delivered = True


    db.commit()

    db.refresh(message)


    return message





# ==========================================================
# MARK MESSAGE SEEN
# ==========================================================

def mark_seen(

    db: Session,

    message_id: int

):

    message = get_message(

        db,

        message_id

    )


    if not message:

        return None



    message.seen = True


    db.commit()

    db.refresh(message)


    return message





# ==========================================================
# ADD ATTACHMENT
# ==========================================================

def add_attachment(

    db: Session,

    message_id: int,

    file_name: str,

    file_url: str,

    file_type: str,

    file_size: int

):

    attachment = Attachment(

        message_id=message_id,

        file_name=file_name,

        file_url=file_url,

        file_type=file_type,

        file_size=file_size

    )


    db.add(attachment)

    db.commit()

    db.refresh(attachment)


    return attachment





# ==========================================================
# GET MESSAGE ATTACHMENTS
# ==========================================================

def get_attachments(

    db: Session,

    message_id: int

):

    return (

        db.query(Attachment)

        .filter(

            Attachment.message_id == message_id

        )

        .all()

    )





# ==========================================================
# CREATE IMAGE MESSAGE
# ==========================================================

def create_image_message(

    db: Session,

    room_id: int,

    user_id: int,

    image_url: str

):

    message = Message(

        room_id=room_id,

        user_id=user_id,

        message_type="image",

        content=None

    )


    db.add(message)

    db.commit()

    db.refresh(message)



    attachment = Attachment(

        message_id=message.id,

        file_name=image_url.split("/")[-1],

        file_url=image_url,

        file_type="image",

        file_size=0

    )


    db.add(attachment)

    db.commit()



    return message





# ==========================================================
# USER ONLINE STATUS
# ==========================================================

def set_user_online(

    db: Session,

    user_id: int

):

    user = (

        db.query(User)

        .filter(

            User.id == user_id

        )

        .first()

    )


    if user:

        user.is_online = True

        db.commit()



    return user





# ==========================================================
# USER OFFLINE STATUS
# ==========================================================

def set_user_offline(

    db: Session,

    user_id: int

):

    user = (

        db.query(User)

        .filter(

            User.id == user_id

        )

        .first()

    )


    if user:

        user.is_online = False


        db.commit()



    return user