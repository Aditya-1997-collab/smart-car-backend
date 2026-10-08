# app/routers/flags.py
from fastapi import APIRouter
from app.models.schemas import FlagUpdateRequest
from app.state import store

router = APIRouter(prefix="/api/features", tags=["Feature Flags"])

@router.get("/flags") # Triggers prefix evaluation matching: /api/features/flags
async def get_feature_flags():
    return store.feature_flags

@router.post("/flags/update")
async def update_feature_flags(updated_flags: FlagUpdateRequest):
    store.feature_flags = updated_flags.model_dump()
    return {"status": "success", "current_flags": store.feature_flags}
