import os
import time
import paho.mqtt.client as mqtt
from app.smart_car.powertrain import VRoboticCarController
from app.state import store
# from app.routers.matrix import store.current_car_controller
from dotenv import load_dotenv

load_dotenv() 

MQTT_BROKER = os.environ["MQTT_BROKER"]
MQTT_PORT = int(os.environ["MQTT_PORT"])
MQTT_USER = os.environ["MQTT_USER"]
MQTT_PASS = os.environ["MQTT_PASS"]

def on_connect(client, userdata, flags, rc):
    """Fires automatically the split second your backend authenticates with EMQX"""
    if rc == 0:
        print("🏆 [MQTT Client] Backend successfully connected to EMQX Cloud Broker Topology!")
        # Subscribe to the upstream sensor metrics topic coming out from the car
        client.subscribe("car/telemetry/radar")
    else:
        print(f"❌ [MQTT Client] Authentication Connection failed with return error code: {rc}")

def on_message(client, userdata, msg):
    """Intercepts live incoming payloads streaming down from the ESP32 car over the air"""
    # global store.current_car_controller
    
    topic = msg.topic
    payload_str = msg.payload.decode("utf-8")
    
    if topic == "car/telemetry/radar":
        try:
            raw_distance = int(payload_str)
            print(f"[MQTT Telemetry Intercept] Raw Sensor Distance: {raw_distance} cm")
            
            # --- RUNTIME SAFETY AUTOMATION BRAIN (Qwen 2.5 Staging Context Target) ---
            # If the matrix is mapped and the car is rushing toward a crash threshold under 20cm:
            if store.current_car_controller is not None and 0 < raw_distance <= 20:
                print("🚨 [CRITICAL SAFETY BRAKE] Obstacle detected locally! Compiling emergency stop payload arrays...")
                
                # Dynamic compile: grabs mapped pins on the fly and generates high-current stop macro commands
                brake_commands = store.current_car_controller.compile_brake()
                
                # Loop through the dynamic instructions and fire them down to the hardware execution topic
                for command in brake_commands:
                    client.publish("car/hardware/execute", command)
                    
        except ValueError:
            print(f"[MQTT Data Error] Received unparsable payload layout profile: {payload_str}")

# Instantiate the absolute master core client connection interface
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
