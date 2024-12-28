from typing import Protocol, List
import logging
import schedule
import time
from .temperature_sensor import TemperatureSensor
from .display_interfaces import DisplayInterface
from weatherApp.models import WeatherConditions, TemperatureRange

logger = logging.getLogger(__name__)


class Controller(Protocol):
    def start_logic(self): ...

    def stop_logic(self): ...


class WeatherConditionsController:
    def __init__(
        self,
        temperature_sensor: TemperatureSensor,
        display_interfaces_list: List[DisplayInterface],
        record_data_period: int,
    ) -> None:
        self.temperature_sensor = temperature_sensor
        self.display_interfaces_list = display_interfaces_list
        self.record_data_period = record_data_period

        self.start_logic()

    def start_logic(self) -> None:
        schedule.every(self.record_data_period).seconds.do(self.display_data)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logger.error("KeyboardInterrupt caught. Closing the controller!")
        finally:
            self.stop_logic()

    def display_data(self) -> None:
        temperature = self.temperature_sensor.get_temperature()
        additional_info = self.temperature_sensor.get_sensor_info()
        data = WeatherConditions(
            temperature=temperature, additional_info=additional_info
        )

        for display_interface in self.display_interfaces_list:
            display_interface.display(data)

    def stop_logic(self) -> None:
        pass
