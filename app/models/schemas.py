# app/models/schemas.py
from pydantic import BaseModel

class FlagUpdateRequest(BaseModel):
    enablePowertrain: bool
    enableDiwaliLighting: bool
    enableCloudAI: bool

class LightingConfig(BaseModel):
    active: bool
    color: str
    intensity: int

class AIPromptRequest(BaseModel):
    prompt: str
