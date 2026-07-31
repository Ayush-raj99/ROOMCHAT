"""
RoomChat V2
Initialize Database
"""

from app.database.database import (
    Base,
    engine,
    SessionLocal
)

from app.models.models import Room

from app.services.security import hash_password



# ==========================================
# CREATE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)



# ==========================================
# DEFAULT ROOMS
# ==========================================

DEFAULT_ROOMS = [

    {
        "name": "General Chat",
        "password": "1234"
    },

    {
        "name": "Study Room",
        "password": "5678"
    },

    {
        "name": "Friends",
        "password": "9999"
    }

]



# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    db = SessionLocal()

    try:

        for room_data in DEFAULT_ROOMS:

            room = (

                db.query(Room)

                .filter(Room.name == room_data["name"])

                .first()

            )

            if room:

                continue


            new_room = Room(

                name=room_data["name"],

                password=hash_password(

                    room_data["password"]

                )

            )

            db.add(new_room)

        db.commit()

        print("✅ Database initialized successfully.")

    except Exception as e:

        db.rollback()

        print(f"❌ Error: {e}")

    finally:

        db.close()



# ==========================================
# RUN FILE
# ==========================================

if __name__ == "__main__":

    initialize_database()