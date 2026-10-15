from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import flags, lighting, ai, websocket, matrix
# Import your newly generated MQTT manager instance hook
from app.mqtt_client import mqtt_client, MQTT_BROKER, MQTT_PORT

app = FastAPI(title="VROBOTIC ESP32 Smart Car Backend Engine Framework")

@app.on_event("startup")
def startup_event():
    """Triggers background tracking loop connections the instant Uvicorn initializes"""
    print("[System Boot] Initializing Asynchronous EMQX MQTT background threads...")
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        # loop_start() spins up a dedicated background thread to handle data traffic seamlessly
        mqtt_client.loop_start()
    except Exception as network_error:
        print(f"⚠️ [MQTT Boot Fail] Could not link cloud network paths: {str(network_error)}")

@app.on_event("shutdown")
def shutdown_event():
    """Cleans up sockets gracefully when the server terminates"""
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("[System Shutdown] Closed all remaining MQTT thread channels.")

# --- The remainder of your clean routing mounts and CORS configurations remain identical ---
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(flags.router)
app.include_router(lighting.router)
app.include_router(ai.router)
app.include_router(websocket.router)
app.include_router(matrix.router) 
