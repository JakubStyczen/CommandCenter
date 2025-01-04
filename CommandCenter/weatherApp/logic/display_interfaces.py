from typing import Protocol, TYPE_CHECKING, Optional
import logging
from weatherApp.models import WeatherConditions
from ExternalModules.LCD_Module_RPI_code_2inch.WaveshareLCD import WaveshareLCD2inch

if TYPE_CHECKING:
    from CommandCenter.config import Config

logger = logging.getLogger(__name__)


class DisplayInterface(Protocol):
    def __init__(self, config: Optional["Config"]) -> None:
        self.config = config

    def display(self, data: WeatherConditions) -> None: ...


class WebAppWeateherDisplayInterface(DisplayInterface):
    def display(self, data: WeatherConditions) -> None:
        data.save()
        logging.debug("Saved WeatherConditions model to database")


class CommandLineWeateherDisplayInterface(DisplayInterface):
    def display(self, data: WeatherConditions) -> None:
        logging.info(str(data))
        logging.debug("Output WeatherConditions data to console")


class LCDWeateherDisplayInterface(DisplayInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config.read_lcd_variables()
        self.lcd_display = WaveshareLCD2inch(
            self.config.lcd_rst,
            self.config.lcd_dc,
            self.config.lcd_bl,
            self.config.spi_dev,
            self.config.spi_bus,
            self.config.font,
        )

    def display(self, data: WeatherConditions) -> None:
        self.lcd_display.wrire_text(f"{data.temperature:.2f}\N{DEGREE SIGN}C")
        logging.debug("Displayed temperature on LCD display")


availavle_display_interfaces = {
    "cmd": CommandLineWeateherDisplayInterface,
    "lcd": LCDWeateherDisplayInterface,
    "web": WebAppWeateherDisplayInterface,
}
