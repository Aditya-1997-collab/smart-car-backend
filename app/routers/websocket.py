import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.state.store import store

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
            try:
                await connection.send_text(text_message)
            except Exception:
                # Safeguard against stale sockets in the broadcast loop
                continue

manager = ConnectionManager()

@router.websocket("/ws/drive")
async def websocket_drive_channel(websocket: WebSocket):
    # 1. Feature Flag Protection Check via the Central State Store
    if not store.feature_flags.get("enablePowertrain", False):
        await websocket.accept()
        await websocket.send_text(json.dumps({"error": "Powertrain engine disabled by Feature Flags."}))
        await websocket.close()
        return

    await manager.connect(websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            parsed_packet = json.loads(raw_data)
            
            # Extract incoming payload (e.g., "FORWARD", "REVERSE", "LEFT", "RIGHT", "STOP")
            user_action = parsed_packet.get('payload', 'STOP')
            print(f"[WebSocket Received] Action Type: {parsed_packet.get('type')}, Payload: {user_action}")
            
            # 2. Hardware Configuration Verification Guard
            if CURRENT_CAR_CONTROLLER is None:
                error_telemetry = {
                    "frontDistance": 0,
                    "rearBlocked": False,
                    "activeState": "ERROR_CONFIG_MISSING",
                    "errorMessage": "Hardware Matrix not initialized. Map your pin configurations via the dashboard first."
                }
                await websocket.send_text(json.dumps(error_telemetry))
                continue

            # 3. Dynamic Low-Level Command Translation Layer
            compiled_commands = []
            try:
                if user_action == "FORWARD":
                    compiled_commands = store.current_car_controller.compile_forward(speed=150)
                elif user_action == "REVERSE":
                    compiled_commands = store.current_car_controller.compile_reverse(speed=120)
                elif user_action == "LEFT":
                    compiled_commands = store.current_car_controller.compile_rotate_left(speed=150)
                elif user_action == "RIGHT":
                    compiled_commands = store.current_car_controller.compile_rotate_right(speed=150)
                elif user_action == "STOP":
                    compiled_commands = store.current_car_controller.compile_brake()

                # 4. Command Dispatch Pipeline Execution Placeholder
                # These are the raw "DW:PIN:VAL" machine strings generated from your frontend mappings
                for command in compiled_commands:
                # 1. PUSH TO THE CLOUD OVER THE AIR
                    try:
                        from app.mqtt_client import mqtt_client
                        mqtt_client.publish("car/hardware/execute", command)
                    except Exception as mqtt_err:
                        print(f"⚠️ [MQTT Publish Fail]: {mqtt_err}")


            except KeyError as config_error:
                # Fallback if an essential component pin was left completely unmapped
                print(f"[Configuration Error] Action blocked: {str(config_error)}")
                await websocket.send_text(json.dumps({
                    "frontDistance": 0, "rearBlocked": False, "activeState": "ERROR_UNMAPPED_PIN", "errorMessage": str(config_error)
                }))
                continue

            # 5. Broadcast Updated Telemetry State Matrix Back to Dashboard Panels
            simulated_telemetry = {
                "frontDistance": 45,
                "rearBlocked": False,
                "activeState": user_action
            }
            await manager.broadcast_to_all(json.dumps(simulated_telemetry))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
