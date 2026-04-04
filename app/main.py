from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(plan_router)
app.include_router(sub_router)
app.include_router(content_router)
app.include_router(access_router)

@app.get("/")
def root():
    return {"status": "API running"}