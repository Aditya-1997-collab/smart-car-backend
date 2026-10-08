# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import flags, lighting, ai, websocket


app = FastAPI(title="VROBOTIC ESP32 Smart Car Backend Engine Framework")

# Clean Application Root Status Welcome Node
@app.get("/")
async def root_welcome():
    return {"system": "VROBOTIC ESP32 Smart Car Backend Engine", "status": "Online/Operational"}

# Configure CORS Middleware cross-origin parameters
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all external modular routers into the orchestrator pipeline core
app.include_router(flags.router)
app.include_router(lighting.router)
app.include_router(ai.router)
app.include_router(websocket.router) # Websocket router maps directly under root
