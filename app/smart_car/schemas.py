from dataclasses import dataclass
from typing import Dict, List, Optional
from pydantic import BaseModel

# 1. Pydantic validation schema matching the React Frontend output structure
class PinMappingIn(BaseModel):
    pinName: str
    pinNumber: str
    isCustom: bool

# 2. Strong-typed internal object for machine computing protection
@dataclass
class HardwareMatrix:
    # A fast key-value store mapping: e.g., {"TRIGGPIN": 10, "IN1": 7}
    pins: Dict[str, int]

    @classmethod
    def from_frontend_payload(cls, payload: List[dict]) -> "HardwareMatrix":
        """Converts raw json array from front-end into clean lookup dictionary"""
        pin_dict = {}
        for row in payload:
            name = row["pinName"].strip().upper()
            try:
                number = int(row["pinNumber"])
                pin_dict[name] = number
            except (ValueError, KeyError):
                continue # Skip corrupted rows safely
        return cls(pins=pin_dict)
