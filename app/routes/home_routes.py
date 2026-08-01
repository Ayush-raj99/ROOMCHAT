"""
RoomChat V2
Home Routes

Shows:
- Available rooms
- Room joining page
"""

from fastapi import APIRouter, Request, Depends
from app.templates_engine import templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Room


router = APIRouter(
    tags=["Home"]
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