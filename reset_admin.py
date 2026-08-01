from app.database.database import SessionLocal
from app.models.models import User
from app.services.security import hash_password


db = SessionLocal()


admin = db.query(User).filter(
    User.username == "admin"
).first()


if admin:

    admin.password = hash_password("12345678")

    db.commit()

    print("Admin password reset successfully")

    print("Username: admin")

    print("Password: 12345678")


else:

    print("Admin account not found")


db.close()