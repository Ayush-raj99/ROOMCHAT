"""
RoomChat V2
Chat WebSocket

Handles:
- Real time text messages
- File messages
- Broadcasting
"""


import json


from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect



from app.websocket.connection_manager import manager


from app.database.database import SessionLocal


from app.services.chat_service import create_message




router = APIRouter()





# ==========================================================
# CHAT SOCKET
# ==========================================================


@router.websocket("/ws/{room_id}/{user_id}")

async def chat_socket(

    websocket: WebSocket,

    room_id: int,

    user_id: int

):


    db = SessionLocal()



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



            message_type = message_data.get(

                "type",

                "text"

            )



            # ==============================
            # TEXT MESSAGE
            # ==============================


            if message_type == "text":



                content = message_data.get(

                    "content"

                )



                if not content:

                    continue





                message = create_message(

                    db,

                    room_id,

                    user_id,

                    content=content

                )







                response = {


                    "type":"text",


                    "user_id":user_id,


                    "content":content,


                    "message_id":message.id


                }





                await manager.broadcast(

                    json.dumps(response),

                    room_id

                )








            # ==============================
            # IMAGE MESSAGE
            # ==============================


            elif message_type == "image":




                image_url = message_data.get(

                    "url"

                )




                if not image_url:

                    continue





                message = create_message(

                    db,

                    room_id,

                    user_id,

                    file_path=image_url,

                    is_image=True

                )






                response = {


                    "type":"image",


                    "user_id":user_id,


                    "url":image_url,


                    "message_id":message.id


                }





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