# app/routers/lighting.py
from fastapi import APIRouter
from app.models.schemas import LightingConfig
from app.state import store

router = APIRouter(prefix="/api/lighting", tags=["Diwali Illumination Layout"])

@router.post("/config")
async def receive_lighting_config(config: LightingConfig):
    store.current_lighting_state = config.model_dump()
    print(f"[HTTP] Modular Update - Diwali LED Configuration Sync: {store.current_lighting_state}")
    return {"status": "synchronized", "payload": store.current_lighting_state}

@router.get("/config")
async def get_lighting_config():
    return store.current_lighting_state
