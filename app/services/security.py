"""
RoomChat V2
Security Service
"""

import bcrypt



# ==============================
# HASH PASSWORD
# ==============================

def hash_password(password: str):

    password_bytes = password.encode("utf-8")

    # bcrypt limit
    password_bytes = password_bytes[:72]

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")



# ==============================
# VERIFY PASSWORD
# ==============================

def verify_password(
    plain_password: str,
    hashed_password: str
):

    password_bytes = plain_password.encode("utf-8")

    password_bytes = password_bytes[:72]


    return bcrypt.checkpw(
        password_bytes,
        hashed_password.encode("utf-8")
    )