"""
RoomChat V2

Main Application

Features:
- Rooms
- Users
- Admin panel
- Chat
- WebSocket
- File upload
"""


from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware


from app.database.database import Base
from app.database.database import engine



from app.routes import home_routes
from app.routes import room_routes
from app.routes import admin_routes
from app.routes import chat_routes
from app.routes import upload_routes



from app.websocket import chat_socket





# ==================================================
# DATABASE TABLE CREATION
# ==================================================


Base.metadata.create_all(

    bind=engine

)







# ==================================================
# FASTAPI APP
# ==================================================


app = FastAPI(

    title="RoomChat V2"

)







# ==================================================
# CORS
# ==================================================


app.add_middleware(

    CORSMiddleware,


    allow_origins=["*"],


    allow_credentials=True,


    allow_methods=["*"],


    allow_headers=["*"]

)







# ==================================================
# STATIC FILES
# ==================================================


app.mount(

    "/static",

    StaticFiles(

        directory="app/static"

    ),

    name="static"

)








# ==================================================
# UPLOADED FILES
# ==================================================


app.mount(

    "/uploads",

    StaticFiles(

        directory="app/uploads"

    ),

    name="uploads"

)









# ==================================================
# NORMAL ROUTES
# ==================================================


app.include_router(

    home_routes.router

)



app.include_router(

    room_routes.router

)



app.include_router(

    admin_routes.router

)



app.include_router(

    chat_routes.router

)



app.include_router(

    upload_routes.router

)








# ==================================================
# WEBSOCKET
# ==================================================


app.include_router(

    chat_socket.router

)









# ==================================================
# TEST ROUTE
# ==================================================


@app.get("/test")

def test():


    return {


        "status":

        "RoomChat V2 running"



    }