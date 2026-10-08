# app/routers/websocket.py
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.state import store

router = APIRouter(tags=["Ultra Low-Latency Powertrain"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"[WebSocket] Connected a new client loop node. Total active links: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"[WebSocket] Terminated a client line. Remainder active links: {len(self.active_connections)}")

    async def broadcast_to_all(self, text_message: str):
        for connection in self.active_connections:
            await connection.send_text(text_message)

manager = ConnectionManager()

@router.websocket("/ws/drive")
async def websocket_drive_channel(websocket: WebSocket):
    if not store.feature_flags["enablePowertrain"]:
        await websocket.accept()
        await websocket.send_text(json.dumps({"error": "Powertrain engine disabled by Feature Flags."}))
        await websocket.close()
        return

    await manager.connect(websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            parsed_packet = json.loads(raw_data)
            print(f"[WebSocket Received] Action Type: {parsed_packet.get('type')}, Payload: {parsed_packet.get('payload')}")
            
            simulated_telemetry = {
                "frontDistance": 45,
                "rearBlocked": False,
                "activeState": parsed_packet.get('payload', 'STOP')
            }
            await manager.broadcast_to_all(json.dumps(simulated_telemetry))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
