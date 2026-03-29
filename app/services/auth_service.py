from app.repositories.user_repository import *
from app.core.security import *

def register(user):
    if get_user_by_mobile(user.mobile_number):
        raise Exception("User exists")

    user_data = {
        "mobile_number": user.mobile_number,
        "password": hash_password(user.password),
        "role": "customer",
        "is_active": True
    }

    create_user(user_data)
    return {"msg": "registered"}

def login(user):
    db_user = get_user_by_mobile(user.mobile_number)

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise Exception("Invalid credentials")

    token = create_token({
        "user_id": str(db_user["_id"]),
        "role": db_user["role"]
    })

    return {"access_token": token}