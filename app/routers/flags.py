# app/routers/flags.py
from fastapi import APIRouter
from app.models.schemas import FlagUpdateRequest
# FIXED IMPORT SYNTAX: Explicitly target the object inside the app.state module namespace
from app.state.store import store 

router = APIRouter(prefix="/api/features", tags=["Feature Flags"])

@router.get("/flags") 
async def get_feature_flags():
    # Now it cleanly locates the dictionary without confusing it for a file folder
    return store.feature_flags

@router.post("/flags/update")
async def update_feature_flags(updated_flags: FlagUpdateRequest):
    store.feature_flags = updated_flags.model_dump()
    return {"status": "success", "current_flags": store.feature_flags}
