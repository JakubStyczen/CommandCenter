from django.test import TestCase, tag
from weatherApp.logic.temperature_sensor import W1TemperatureSensor


@tag("only_local")
class TestW1TemperatureSensor(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.temperature_sensor = W1TemperatureSensor()

    def test_get_temperature(self) -> None:
        measured_temperature = self.temperature_sensor.get_temperature()
        self.assertTrue(type(measured_temperature) == float)
        self.assertTrue(
            self.temperature_sensor.lower_band
            < measured_temperature
            < self.temperature_sensor.upper_band
        )

    def test_get_sensor_info(self) -> None:
        self.assertTrue(
            "Captured with 1 wire DS18B20 sesnor"
            == self.temperature_sensor.get_sensor_info()
        )
