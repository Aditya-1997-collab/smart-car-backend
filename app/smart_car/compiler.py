from typing import Optional

class MQTTCommandCompiler:
    """Translates abstract hardware interactions into thin-client machine string arrays"""
    
    @staticmethod
    def digital_write(pin: Optional[int], value: int) -> str:
        if pin is None:
            raise ValueError("Target pin not mapped in Matrix Configuration.")
        # Outputs structural design matching the client parser: "DW:PIN:VALUE"
        return f"DW:{pin}:{1 if value else 0}"

    @staticmethod
    def analog_write(pin: Optional[int], value: int) -> str:
        if pin is None:
            raise ValueError("Target pin not mapped in Matrix Configuration.")
        # Enforce strict 8-bit boundary checks for hardware safety
        value = max(0, min(255, value))
        return f"AW:{pin}:{value}"

    @staticmethod
    def ultrasonic_macro(trig_pin: Optional[int], echo_pin: Optional[int]) -> str:
        if trig_pin is None or echo_pin is None:
            raise ValueError("Ultrasonic pins missing in current matrix configurations.")
        return f"US:{trig_pin}:{echo_pin}"
