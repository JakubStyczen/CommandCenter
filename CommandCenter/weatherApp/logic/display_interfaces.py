from typing import Protocol
import logging
from weatherApp.models import WeatherConditions

logger = logging.getLogger(__name__)


class DisplayInterface(Protocol):
    def display(self, data: WeatherConditions) -> None: ...


class WebAppWeateherDisplayInterface:
    def display(self, data: WeatherConditions) -> None:
        data.save()
        logging.info("Saved WeatherConditions model to database")


class CommandLineWeateherDisplayInterface:
    def display(self, data: WeatherConditions) -> None:
        logging.info(str(data))


class LCDWeateherDisplayInterface:
    def display(self, data: WeatherConditions) -> None:
        pass
