"""
RoomChat V2
Chat Service

Handles:
- Creating messages
- File messages
- Getting chat history
"""


from sqlalchemy.orm import Session

from app.models.models import Message





# ==========================================================
# CREATE MESSAGE
# ==========================================================

def create_message(

    db: Session,

    room_id: int,

    user_id: int,

    content: str = None,

    file_name: str = None,

    file_path: str = None,

    is_image: bool = False

):


    message = Message(

        room_id=room_id,

        user_id=user_id,

        content=content,

        file_name=file_name,

        file_path=file_path,

        is_image=is_image

    )



    db.add(message)

    db.commit()

    db.refresh(message)



    return {

        "id": message.id,

        "room_id": message.room_id,

        "user_id": message.user_id,

        "content": message.content,

        "file_name": message.file_name,

        "file_path": message.file_path,

        "is_image": message.is_image,

        "created_at": message.created_at.isoformat()

    }







# ==========================================================
# GET ROOM MESSAGES
# ==========================================================

def get_room_messages(

    db: Session,

    room_id: int

):


    messages = db.query(Message).filter(

        Message.room_id == room_id

    ).order_by(

        Message.created_at.asc()

    ).all()



    result = []



    for message in messages:


        result.append({

            "id": message.id,

            "room_id": message.room_id,

            "user_id": message.user_id,

            "content": message.content,

            "file_name": message.file_name,

            "file_path": message.file_path,

            "is_image": message.is_image,

            "created_at": message.created_at.isoformat()

        })



    return result