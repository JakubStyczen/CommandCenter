from unittest.mock import Mock
from django.test import TestCase, tag
from contextlib import redirect_stdout
from io import StringIO
import logging
from weatherApp.models import WeatherConditions
from weatherApp.logic.temperature_sensor import W1TemperatureSensor, TemperatureSensor
from weatherApp.logic.display_interfaces import (
    DisplayInterface,
    WebAppWeateherDisplayInterface,
    availavle_display_interfaces,
)
from weatherApp.logic.controller import (
    WeatherConditionsController,
    WeatherConditionsMainLogic,
)
from CommandCenter.config import Config


@tag("only_local")
class TestWeatherConditionsController(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.mock_temperature_sensor = Mock(spec=TemperatureSensor)
        cls.mock_temperature_sensor.get_temperature.return_value = 0
        cls.mock_temperature_sensor.get_sensor_info.return_value = "MockedSensor"
        cls.mock_display_interface = Mock(spec=DisplayInterface)
        cls.mock_display_interface.display = lambda data: print("Success")

    def test_display_data(self) -> None:
        # redirect stderr from logging to StringIO
        out = StringIO()
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(out)
        root.addHandler(handler)
        controller = WeatherConditionsController(
            self.mock_temperature_sensor, [self.mock_display_interface], 10
        )
        with redirect_stdout(out):
            result = controller.display_data()
        self.assertIn("Success", out.getvalue())
