from django.test import TestCase
from contextlib import redirect_stdout
from unittest.mock import Mock
from io import StringIO
import logging
from weatherApp.models import WeatherConditions
from weatherApp.logic.display_interfaces import (
    WebAppWeateherDisplayInterface,
    CommandLineWeateherDisplayInterface,
    LCDWeateherDisplayInterface,
)
from CommandCenter.config import Config


class TestWebAppWeateherDisplayInterface(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.config = Mock(spec=Config)
        cls.web_app_display = WebAppWeateherDisplayInterface(cls.config)

    def test_web_display(self) -> None:
        weather_condition = WeatherConditions(
            temperature=5, additional_info="Testing info"
        )
        self.web_app_display.display(weather_condition)
        self.assertTrue(WeatherConditions.objects.filter(temperature="5").exists())

    def test_web_display_catches_integrity_error(self) -> None:
        # redirect stderr from logging to StringIO
        out = StringIO()
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(out)
        root.addHandler(handler)
        weather_condition_wrong_temp = WeatherConditions(
            temperature=125.01, additional_info="Testing info"
        )
        with redirect_stdout(out):
            self.web_app_display.display(weather_condition_wrong_temp)
        self.assertIn("Invalid data while saving to database", out.getvalue())


class TestCommandLineWeateherDisplayInterface(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.config = Mock(spec=Config)
        cls.cmd_display = CommandLineWeateherDisplayInterface(cls.config)

    def test_web_display(self) -> None:
        # redirect stdout from logging to StringIO
        out = StringIO()
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(out)
        root.addHandler(handler)
        weather_condition = WeatherConditions(
            temperature=5, additional_info="Testing info"
        )
        with redirect_stdout(out):
            self.cmd_display.display(weather_condition)
        self.assertIn(str(weather_condition), out.getvalue())
        self.assertIn("Output WeatherConditions data to console", out.getvalue())

    def test_web_display_catches_validation_error(self) -> None:
        # redirect stdout from logging to StringIO
        out = StringIO()
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(out)
        root.addHandler(handler)
        weather_condition = WeatherConditions(
            temperature=125.01, additional_info="Testing info"
        )
        with redirect_stdout(out):
            self.cmd_display.display(weather_condition)
        self.assertIn("Invalid data", out.getvalue())

    def test_validate_data(self) -> None:
        weather_condition = WeatherConditions(
            temperature=5, additional_info="Testing info"
        )
        self.assertTrue(self.cmd_display.validate_data(weather_condition))

    def test_validate_wrong_data(self) -> None:
        weather_condition = WeatherConditions(
            temperature=125.01, additional_info="Testing info"
        )
        self.assertFalse(self.cmd_display.validate_data(weather_condition))
