from app.repositories.content_repository import *
from fastapi import HTTPException

def add_content(content):
    try:
        result = create_content(content.dict())
        return {"message": "Content added successfully", "content_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_content():
    try:
        contents = get_all_content()
        for content in contents:
            if "_id" in content:
                content["_id"] = str(content["_id"])
        return contents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))