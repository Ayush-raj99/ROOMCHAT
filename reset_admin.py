from app.database.database import SessionLocal
from app.models.models import User
from app.services.security import hash_password


db = SessionLocal()

admin = db.query(User).filter(
    User.username == "admin"
).first()


if admin:
    admin.password = hash_password("NewPassword123")
    db.commit()
    print("Admin password changed")
else:
    print("Admin not found")


db.close()