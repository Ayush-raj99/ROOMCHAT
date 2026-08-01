"""
RoomChat V2

Main Application
"""


from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware


from app.database.database import (
    Base,
    engine,
    SessionLocal
)


from app.models.models import (
    Room,
    RoomMember
)



from app.routes import (
    home_routes,
    room_routes,
    admin_routes,
    chat_routes,
    upload_routes
)



from app.websocket import chat_socket


from app.services.security import verify_password





# ==========================================
# DATABASE
# ==========================================


Base.metadata.create_all(
    bind=engine
)






# ==========================================
# FASTAPI APP
# ==========================================


app = FastAPI(
    title="RoomChat V2"
)






# ==========================================
# CORS
# ==========================================


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)







# ==========================================
# STATIC FILES
# ==========================================


app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static"

)





# Uploaded files


app.mount(

    "/uploads",

    StaticFiles(
        directory="app/uploads"
    ),

    name="uploads"

)








# ==========================================
# DEBUG
# ==========================================



@app.get("/debug-room/{room_id}")
def debug_room(room_id:int):


    db = SessionLocal()


    try:


        room = db.query(Room).filter(
            Room.id == room_id
        ).first()



        if not room:

            return {
                "error":"Room not found"
            }




        return {

            "id":room.id,

            "name":room.name,

            "password_hash":room.password

        }


    finally:

        db.close()







@app.get("/test-password/{room_id}/{password}")
def test_password(
    room_id:int,
    password:str
):


    db = SessionLocal()


    try:


        room = db.query(Room).filter(
            Room.id == room_id
        ).first()



        if not room:

            return {
                "error":"Room not found"
            }




        return {


            "entered_password":password,


            "verify_result":
            verify_password(

                password,

                room.password

            )

        }



    finally:

        db.close()








@app.get("/check-members")
def check_members():


    db = SessionLocal()


    try:


        members = db.query(
            RoomMember
        ).all()



        return [

            {

                "id":m.id,

                "user_id":m.user_id,

                "room_id":m.room_id

            }

            for m in members

        ]


    finally:

        db.close()







# ==========================================
# ROUTERS
# ==========================================


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


app.include_router(
    chat_socket.router
)






# ==========================================
# TEST
# ==========================================


@app.get("/test")
def test():

    return {

        "status":
        "RoomChat V2 running"

    }