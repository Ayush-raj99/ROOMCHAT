"""
RoomChat V2
Real-time Chat WebSocket
"""

import json

from fastapi import (
    WebSocket,
    WebSocketDisconnect
)

from sqlalchemy.orm import Session


from app.websocket.connection_manager import manager

from app.database.database import SessionLocal

from app.services.chat_service import create_message





# ==========================================================
# CHAT SOCKET
# ==========================================================

async def chat_socket(

    websocket: WebSocket,

    room_id: int,

    user_id: int

):

    db: Session = SessionLocal()


    await manager.connect(

        websocket,

        room_id

    )


    try:

        while True:


            data = await websocket.receive_text()


            message_data = json.loads(

                data

            )


            content = message_data.get(

                "content"

            )



            # Save message

            message = create_message(

                db,

                room_id,

                user_id,

                content

            )



            response = {

                "id": message.id,

                "room_id": room_id,

                "user_id": user_id,

                "content": content,

                "type": "message"

            }



            # Send to everyone in room

            await manager.broadcast(

                json.dumps(response),

                room_id

            )



    except WebSocketDisconnect:


        manager.disconnect(

            websocket,

            room_id

        )


    finally:

        db.close()