from typing import List
from .schemas import HardwareMatrix
from .compiler import MQTTCommandCompiler

class VRoboticCarController:
    """The absolute brain of the car. Compiles high-level actions dynamically 
    based on the loaded matrix profile configuration maps."""
    
    def __init__(self, matrix: HardwareMatrix):
        self.matrix = matrix
        self.compiler = MQTTCommandCompiler()

    def _get_pin(self, name: str) -> int:
        """Helper to fetch a specific pin safely, raising an alert if unmapped."""
        pin = self.matrix.pins.get(name.upper())
        if pin is None:
            raise KeyError(f"Critical configuration missing: Pin '{name.upper()}' is not mapped.")
        return pin

    def compile_forward(self, speed: int = 150) -> List[str]:
        """Compiles clean dynamic arrays to move the car forward safely."""
        return [
            # 1. Dispatch dynamic motor speed configurations via PWM
            self.compiler.analog_write(self._get_pin("ENA"), speed),
            self.compiler.analog_write(self._get_pin("ENB"), speed),
            # 2. Standard L298N directional parameters from context document
            self.compiler.digital_write(self._get_pin("IN1"), 1),
            self.compiler.digital_write(self._get_pin("IN2"), 0),
            self.compiler.digital_write(self._get_pin("IN3"), 1),
            self.compiler.digital_write(self._get_pin("IN4"), 0),
        ]

    def compile_reverse(self, speed: int = 120) -> List[str]:
        return [
            self.compiler.analog_write(self._get_pin("ENA"), speed),
            self.compiler.analog_write(self._get_pin("ENB"), speed),
            self.compiler.digital_write(self._get_pin("IN1"), 0),
            self.compiler.digital_write(self._get_pin("IN2"), 1),
            self.compiler.digital_write(self._get_pin("IN3"), 0),
            self.compiler.digital_write(self._get_pin("IN4"), 1),
        ]

    def compile_rotate_left(self, speed: int = 150) -> List[str]:
        return [
            self.compiler.analog_write(self._get_pin("ENA"), speed),
            self.compiler.analog_write(self._get_pin("ENB"), speed),
            self.compiler.digital_write(self._get_pin("IN1"), 0),
            self.compiler.digital_write(self._get_pin("IN2"), 1),
            self.compiler.digital_write(self._get_pin("IN3"), 1),
            self.compiler.digital_write(self._get_pin("IN4"), 0),
        ]

    def compile_rotate_right(self, speed: int = 150) -> List[str]:
        return [
            self.compiler.analog_write(self._get_pin("ENA"), speed),
            self.compiler.analog_write(self._get_pin("ENB"), speed),
            self.compiler.digital_write(self._get_pin("IN1"), 1),
            self.compiler.digital_write(self._get_pin("IN2"), 0),
            self.compiler.digital_write(self._get_pin("IN3"), 0),
            self.compiler.digital_write(self._get_pin("IN4"), 1),
        ]

    def compile_brake(self) -> List[str]:
        """Core Project Rule: 200ms Active electronic braking counteracting back-EMF 
        inertia is executed downstream dynamically on the ESP32 via high-current values."""
        return [
            self.compiler.analog_write(self._get_pin("ENA"), 0),
            self.compiler.analog_write(self._get_pin("ENB"), 0),
            self.compiler.digital_write(self._get_pin("IN1"), 1),
            self.compiler.digital_write(self._get_pin("IN2"), 1),
            self.compiler.digital_write(self._get_pin("IN3"), 1),
            self.compiler.digital_write(self._get_pin("IN4"), 1),
        ]

    def trigger_radar_pulse(self) -> str:
        """Assembles the atomic microsecond radar routine macro execution instruction."""
        return self.compiler.ultrasonic_macro(
            self._get_pin("TRIGGPIN"), 
            self._get_pin("ECHOPIN")
        )
