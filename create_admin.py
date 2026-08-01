from app.database.database import SessionLocal
from app.models.models import User
from app.services.security import hash_password


db = SessionLocal()


existing = db.query(User).filter(
    User.username == "admin"
).first()


if existing:

    print("Admin already exists")


else:

    admin = User(

        username="AYUSH RAJ",

        password=hash_password("Ayuraj"),

        role="admin"

    )


    db.add(admin)

    db.commit()

    db.refresh(admin)


    print("Admin created")

    print("Username: AYUSH RAJ")

    print("Password: Ayuraj")



db.close()