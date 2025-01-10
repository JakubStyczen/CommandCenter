from typing import Protocol, List
import logging
import schedule
import time
import threading
from weatherApp.models import WeatherConditions
from weatherApp.logic.temperature_sensor import W1TemperatureSensor, TemperatureSensor
from weatherApp.logic.display_interfaces import (
    DisplayInterface,
    WebAppWeateherDisplayInterface,
    availavle_display_interfaces,
)
from CommandCenter.config import Config

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

    def start_logic(self, is_stopped) -> None:
        schedule.every(self.record_data_period).seconds.do(self.display_data)
        try:
            while not is_stopped():
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


class WeatherConditionsMainLogic(threading.Thread):
    def __init__(
        self,
        display_interfaces_list_str: list[str] | None,
        config: Config,
        temperature_sensor: TemperatureSensor = W1TemperatureSensor(),
    ) -> None:
        super().__init__(daemon=True)
        self.config = config
        self._stop_event = threading.Event()
        self.display_interfaces_list: list[DisplayInterface] = (
            self.prepare_display_interfaces(display_interfaces_list_str)
        )
        self.temperature_sensor = temperature_sensor
        self.controller: Controller = WeatherConditionsController(
            self.temperature_sensor,
            self.display_interfaces_list,
            self.config.record_data_period,
        )

    def prepare_display_interfaces(
        self, display_interfaces_list_str: list[str] | None
    ) -> list[DisplayInterface]:
        default_display_interfaces_list: list[DisplayInterface] = [
            WebAppWeateherDisplayInterface(self.config)
        ]
        if display_interfaces_list_str is None:
            return default_display_interfaces_list
        for interface_name in set(display_interfaces_list_str):
            display_interface = availavle_display_interfaces.get(
                interface_name.lower(), None
            )
            if display_interface is not None:
                default_display_interfaces_list.append(display_interface(self.config))
        return default_display_interfaces_list

    def run(self):
        self.controller.start_logic(self._stop_event.is_set)

    def stop(self):
        self._stop_event.set()
