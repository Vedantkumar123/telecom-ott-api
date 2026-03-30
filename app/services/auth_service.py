from app.repositories.user_repository import *
from app.core.security import *
from fastapi import HTTPException

def register(user):
    try:
        existing_user = get_user_by_mobile(user.mobile_number)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        user_data = {
            "mobile_number": user.mobile_number,
            "password": hash_password(user.password),
            "role": user.role,
            "is_active": True
        }

        result = create_user(user_data)
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def login(user):
    try:
        db_user = get_user_by_mobile(user.mobile_number)

        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_token({
            "user_id": str(db_user["_id"]),
            "role": db_user["role"]
        })

        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))