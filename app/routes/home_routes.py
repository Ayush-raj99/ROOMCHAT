"""
RoomChat V2
Home Routes

Shows:
- Available rooms
- Room joining page
"""

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Room


router = APIRouter(
    tags=["Home"]
)


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/")
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    rooms = db.query(Room).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rooms": rooms
        }
    )