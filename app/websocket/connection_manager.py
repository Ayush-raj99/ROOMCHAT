"""
RoomChat V2
WebSocket Connection Manager

Handles:
- Active users
- Room connections
- Broadcasting messages
"""


from typing import Dict, List

from fastapi import WebSocket



# ==========================================================
# CONNECTION MANAGER
# ==========================================================


class ConnectionManager:


    def __init__(self):


        self.connections: Dict[

            int,

            List[WebSocket]

        ] = {}



    # ======================================================
    # CONNECT USER
    # ======================================================

    async def connect(

        self,

        websocket: WebSocket,

        room_id:int

    ):


        await websocket.accept()



        if room_id not in self.connections:


            self.connections[room_id] = []



        self.connections[room_id].append(

            websocket

        )



    # ======================================================
    # DISCONNECT USER
    # ======================================================

    def disconnect(

        self,

        websocket:WebSocket,

        room_id:int

    ):


        if room_id in self.connections:


            if websocket in self.connections[room_id]:


                self.connections[room_id].remove(

                    websocket

                )



            if len(self.connections[room_id]) == 0:


                del self.connections[room_id]



    # ======================================================
    # SEND MESSAGE TO ROOM
    # ======================================================

    async def broadcast(

        self,

        message:str,

        room_id:int

    ):


        if room_id not in self.connections:

            return



        for connection in self.connections[room_id]:


            await connection.send_text(

                message

            )



# ==========================================================
# GLOBAL OBJECT
# ==========================================================

manager = ConnectionManager()