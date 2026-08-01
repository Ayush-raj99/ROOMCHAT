"""
RoomChat V2
Home Routes
"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Room
from app.templates_engine import templates


router = APIRouter(
    tags=["Home"]
)


@router.api_route("/", methods=["GET", "HEAD"])
def home(
    request: Request,
    db: Session = Depends(get_db)
):

    rooms = db.query(Room).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "rooms": rooms
        }
    )