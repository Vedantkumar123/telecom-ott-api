from fastapi import FastAPI
from bson import ObjectId

from app.controllers.auth_controller import router as auth_router
from app.controllers.plan_controller import router as plan_router
from app.controllers.subscription_controller import router as sub_router
from app.controllers.content_controller import router as content_router
from app.controllers.access_controller import router as access_router

app = FastAPI(
    title="Telecom OTT API",
    json_encoders={
        ObjectId: str
    }
)

app.include_router(auth_router)
app.include_router(plan_router)
app.include_router(sub_router)
app.include_router(content_router)
app.include_router(access_router)

@app.get("/")
def root():
    return {"status": "API running"}