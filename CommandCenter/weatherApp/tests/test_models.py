from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from weatherApp.models import WeatherConditions, TemperatureRange


class TestWeatherConditionsModel(TestCase):
    databases = "__all__"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.weather_conditions = WeatherConditions(
            temperature=5, additional_info="Testing info"
        )

    def test_str_conversion(self) -> None:
        str_representation = f"Weather conditions captured at: {self.weather_conditions.time}. Temerature: {self.weather_conditions.temperature}\N{DEGREE SIGN} {self.weather_conditions.temperature_emoji.value}. {self.weather_conditions.additional_info}"
        self.assertEqual(str(self.weather_conditions), str_representation)

    def test_default_date_creation(self) -> None:
        self.assertIsNone(self.weather_conditions.time)
        self.weather_conditions.save()
        self.assertIsNotNone(self.weather_conditions.time)

    def test_temperature_out_of_range_raises_exception(self) -> None:
        below_range = WeatherConditions(temperature=-55.01)
        with self.assertRaises(ValidationError):
            below_range.clean()
        above_range = WeatherConditions(temperature=125.01)
        with self.assertRaises(ValidationError):
            above_range.clean()

    def test_temperature_below_constrains(self) -> None:
        below_range = WeatherConditions(temperature=-55.01)
        with self.assertRaises(IntegrityError):
            below_range.save()

    def test_temperature_above_constrains(self) -> None:
        above_range = WeatherConditions(temperature=125.01)
        with self.assertRaises(IntegrityError):
            above_range.save()

    def test_get_temperature_emoji(self) -> None:
        self.weather_conditions.temperature = -11
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.FREEZING
        )
        self.weather_conditions.temperature = -1
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.COLD
        )
        self.weather_conditions.temperature = 12
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.COOL
        )
        self.weather_conditions.temperature = 17
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.MILD
        )
        self.weather_conditions.temperature = 28
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.WARM
        )
        self.weather_conditions.temperature = 34
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.HOT
        )
        self.weather_conditions.temperature = 36
        self.assertEqual(
            self.weather_conditions.temperature_emoji, TemperatureRange.SCHORCHING
        )
