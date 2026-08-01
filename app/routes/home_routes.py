"""
RoomChat V2
Home Routes

Handles:
- Main website page
- Showing available rooms
"""


from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session


from app.database.database import get_db

from app.services.room_service import get_all_rooms



# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter()



# ==========================================================
# TEMPLATE LOCATION
# ==========================================================

templates = Jinja2Templates(

    directory="app/templates"

)



# ==========================================================
# HOME PAGE
# ==========================================================

@router.get("/")

def home(

    request: Request,

    db: Session = Depends(get_db)

):


    rooms = get_all_rooms(

        db

    )


    return templates.TemplateResponse(

        "index.html",

        {

            "request": request,

            "rooms": rooms

        }

    )