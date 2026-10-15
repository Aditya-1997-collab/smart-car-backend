# app/state/store.py
from typing import Optional
# Import your powertrain controller class
from app.smart_car.powertrain import VRoboticCarController

class AppState:
    def __init__(self):
        self.feature_flags = {
            "enablePowertrain": True,
            "enableDiwaliLighting": True,
            "enableCloudAI": True
        }
        # 1. ADD THIS LINE: Centralized storage node for memory state persistence
        self.current_car_controller: Optional[VRoboticCarController] = None

# Initialize your single central instance
store = AppState()

