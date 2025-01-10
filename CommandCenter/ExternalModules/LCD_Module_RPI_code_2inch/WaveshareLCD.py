import os
import time
import logging
import spidev as SPI
from ExternalModules.LCD_Module_RPI_code_2inch.lib import LCD_2inch
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass

logger = logging.getLogger(__name__)

FONTS_PATH = "ExternalModules/LCD_Module_RPI_code_2inch/Font/"


@dataclass
class WaveshareLCD2inch:
    rst_pin: int
    dc_pin: int
    bl_pin: int
    bus_no: int
    device_no: int
    font: str

    def __post_init__(self) -> None:
        # display with hardware SPI:
        """Warning!!!Don't  creation of multiple displayer objects!!!"""
        # disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
        self.display = LCD_2inch.LCD_2inch()
        # Initialize library.
        self.display.Init()
        # Clear display.
        self.display.clear()
        # Set the backlight to 100
        self.display.bl_DutyCycle(50)

        self.display_resolution = (self.display.height, self.display.width)

    def wrire_text(self, text: str, position: tuple[int, int] = (100, 92)) -> None:
        try:
            image_to_display = Image.new("RGB", self.display_resolution, "BLACK")
            draw = ImageDraw.Draw(image_to_display)

            font_path = os.path.join(FONTS_PATH, f"{self.font}.ttf")
            if not os.path.exists(font_path):
                font_path = os.path.join(FONTS_PATH, f"Font01.ttf")
            font_type = ImageFont.truetype(font_path, 50)
            draw.text(position, text, fill="WHITE", font=font_type)
            image_to_display = image_to_display.rotate(180)

            logging.debug("Drawing image...")
            self.display.ShowImage(image_to_display)
        except IOError as e:
            logging.error(e)
        except KeyboardInterrupt:
            self.display.module_exit()
            logging.info("Quiting lcd display handling due to KeyboardInterrupt")
            exit()
