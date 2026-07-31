"""
RoomChat V2
Main FastAPI Application
"""


from fastapi import FastAPI, WebSocket

from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware


from app.database.database import Base, engine


from app.routes import (
    home_routes,
    user_routes,
    room_routes,
    chat_routes,
    upload_routes
)


from app.websocket.chat_socket import chat_socket





# =====================================================
# DATABASE TABLE CREATION
# =====================================================

Base.metadata.create_all(

    bind=engine

)





# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(

    title="RoomChat",

    description="Real-time private chat platform",

    version="2.0"

)





# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)





# =====================================================
# STATIC FILES
# =====================================================

app.mount(

    "/static",

    StaticFiles(

        directory="app/static"

    ),

    name="static"

)



app.mount(

    "/uploads",

    StaticFiles(

        directory="app/uploads"

    ),

    name="uploads"

)





# =====================================================
# HTML ROUTES
# =====================================================

app.include_router(

    home_routes.router

)





# =====================================================
# API ROUTES
# =====================================================

app.include_router(

    user_routes.router

)


app.include_router(

    room_routes.router

)


app.include_router(

    chat_routes.router

)


app.include_router(

    upload_routes.router

)





# =====================================================
# WEBSOCKET CHAT
# =====================================================

@app.websocket(

    "/ws/{room_id}/{user_id}"

)

async def websocket_endpoint(

    websocket: WebSocket,

    room_id: int,

    user_id: int

):


    await chat_socket(

        websocket,

        room_id,

        user_id

    )





# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/api/status")

def status():


    return {

        "status": "running",

        "project": "RoomChat",

        "version": "2.0"

    }