"""
RoomChat V2
WebSocket Connection Manager
"""

from typing import Dict, List

from fastapi import WebSocket





class ConnectionManager:


    def __init__(self):

        self.active_connections: Dict[
            int,
            List[WebSocket]
        ] = {}





    # ======================================================
    # CONNECT USER
    # ======================================================

    async def connect(

        self,

        websocket: WebSocket,

        room_id: int

    ):

        await websocket.accept()


        if room_id not in self.active_connections:

            self.active_connections[room_id] = []


        self.active_connections[room_id].append(

            websocket

        )





    # ======================================================
    # DISCONNECT USER
    # ======================================================

    def disconnect(

        self,

        websocket: WebSocket,

        room_id: int

    ):

        if room_id in self.active_connections:

            if websocket in self.active_connections[room_id]:

                self.active_connections[room_id].remove(

                    websocket

                )


            if not self.active_connections[room_id]:

                del self.active_connections[room_id]





    # ======================================================
    # SEND TO ONE ROOM
    # ======================================================

    async def broadcast(

        self,

        message: str,

        room_id: int

    ):

        if room_id not in self.active_connections:

            return


        for connection in self.active_connections[room_id]:

            await connection.send_text(

                message

            )





# Global manager

manager = ConnectionManager()