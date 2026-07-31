"""
RoomChat V2
Home Page Routes
"""

from fastapi import APIRouter, Request

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates





router = APIRouter(

    tags=["Home"]

)



templates = Jinja2Templates(

    directory="app/templates"

)





# ==========================================================
# HOME PAGE
# ==========================================================

@router.get(

    "/",

    response_class=HTMLResponse

)

async def home(

    request: Request

):

    return templates.TemplateResponse(

        "index.html",

        {

            "request": request

        }

    )





# ==========================================================
# LOGIN PAGE
# ==========================================================

@router.get(

    "/login",

    response_class=HTMLResponse

)

async def login_page(

    request: Request

):

    return templates.TemplateResponse(

        "login.html",

        {

            "request": request

        }

    )





# ==========================================================
# CREATE ROOM PAGE
# ==========================================================

@router.get(

    "/create-room",

    response_class=HTMLResponse

)

async def create_room_page(

    request: Request

):

    return templates.TemplateResponse(

        "create_room.html",

        {

            "request": request

        }

    )





# ==========================================================
# JOIN ROOM PAGE
# ==========================================================

@router.get(

    "/join-room",

    response_class=HTMLResponse

)

async def join_room_page(

    request: Request

):

    return templates.TemplateResponse(

        "join_room.html",

        {

            "request": request

        }

    )





# ==========================================================
# CHAT PAGE
# ==========================================================

@router.get(

    "/chat/{room_id}",

    response_class=HTMLResponse

)

async def chat_page(

    request: Request,

    room_id: int

):

    return templates.TemplateResponse(

        "chat.html",

        {

            "request": request,

            "room_id": room_id

        }

    )