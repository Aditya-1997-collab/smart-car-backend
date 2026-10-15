from fastapi import APIRouter
from app.smart_car.schemas import PinMappingIn, HardwareMatrix
from app.smart_car.powertrain import VRoboticCarController
# Import the central state store instance
from app.state.store import store
from typing import List

router = APIRouter(prefix="/api/hardware", tags=["Hardware Matrix Configuration"])

@router.post("/config")
async def save_hardware_matrix(payload: List[PinMappingIn]):
    # Transform raw frontend pydantic payload array into structured dictionary matrix
    raw_list = [row.dict() for row in payload]
    active_matrix = HardwareMatrix.from_frontend_payload(raw_list)
    
    # SAVE TO CENTRAL MEMORY STORE: Instantiates brain profile into global state singleton
    store.current_car_controller = VRoboticCarController(matrix=active_matrix)
    
    print(f"[System Engine] Loaded new Hardware Matrix Map Profile: {active_matrix.pins}")
    return {"status": "success", "message": "Hardware Pin Matrix compiled and loaded into central server memory."}
