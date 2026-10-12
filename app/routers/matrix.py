from fastapi import APIRouter, HTTPException
from app.smart_car.schemas import PinMappingIn, HardwareMatrix
from app.smart_car.powertrain import VRoboticCarController
from typing import List, Optional

router = APIRouter(prefix="/api/hardware", tags=["Hardware Matrix Configuration"])

# Temporary runtime global storage engine (Replaced by database models tomorrow)
ACTIVE_HARDWARE_MATRIX: Optional[HardwareMatrix] = None
CURRENT_CAR_CONTROLLER: Optional[VRoboticCarController] = None

@router.post("/config")
async def save_hardware_matrix(payload: List["PinMappingIn"]):
    global ACTIVE_HARDWARE_MATRIX, CURRENT_CAR_CONTROLLER
    
    # 1. Transform raw frontend pydantic payload array into structured dictionary matrix
    raw_list = [row.dict() for row in payload]
    ACTIVE_HARDWARE_MATRIX = HardwareMatrix.from_frontend_payload(raw_list)
    
    # 2. Re-instantiate the Car Controller brain with the brand new mapping layout profile
    CURRENT_CAR_CONTROLLER = VRoboticCarController(matrix=ACTIVE_HARDWARE_MATRIX)
    
    print(f"[System Engine] Loaded new Hardware Matrix Map Profile: {ACTIVE_HARDWARE_MATRIX.pins}")
    return {"status": "success", "message": "Hardware Pin Matrix compiled and loaded into server memory."}
