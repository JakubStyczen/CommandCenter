from typing import Protocol
from w1thermsensor import W1ThermSensor
import logging

logger = logging.getLogger(__name__)


class TemperatureSensor(Protocol):
    def get_temperature(self) -> float: ...

    def get_sensor_info(self) -> str: ...


class W1TemperatureSensor:
    def __init__(self) -> None:
        self.temperature_sensor: W1ThermSensor = W1ThermSensor()

    def get_temperature(self) -> float:
        temperature = self.temperature_sensor.get_temperature()
        logger.debug(f"Current temperature: {temperature}\N{DEGREE SIGN}C")
        return temperature

    def get_sensor_info(self) -> str:
        return "Captured with 1 wire dsxxx sesnor"
