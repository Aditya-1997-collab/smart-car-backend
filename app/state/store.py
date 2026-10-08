# app/state/store.py

# Shared memory structures acting as our Single Source of Truth
feature_flags = {
    "enablePowertrain": True,
    "enableDiwaliLighting": True,
    "enableCloudAI": True
}

current_lighting_state = {
    "active": False, 
    "color": "#ffaa00", 
    "intensity": 128
}
