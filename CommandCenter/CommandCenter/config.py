import logging
from environs import Env
from typing import Optional


class Config:
    def __init__(self) -> None:
        self.env = Env()
        self.env.read_env()
        self.logging_level: Optional[int] = None

    def setup_logging(self) -> None:
        self.logging_level: int = logging.getLevelName(
            self.env.str("LOGGING_LEVEL", "INFO")
        )
        logging.basicConfig(
            level=self.logging_level,
            format="[%(asctime)s][%(levelname)s]:  %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def read_env_varaibles(self) -> None:
        self.record_data_period = self.env.int("RECORD_DATA_PERIOD", 120)  # secs

    def read_lcd_variables(self) -> None:
        self.lcd_rst = self.env.int("RST_GPIO", 27)
        self.lcd_dc = self.env.int("DC_GPIO", 25)
        self.lcd_bl = self.env.int("BL_GPIO", 24)
        self.spi_dev = self.env.int("SPI_DEV", 0)
        self.spi_bus = self.env.int("SPI_BUS", 0)
        self.font = self.env.str("FONT", "Font01")
