import sys
from .controller import WeatherConditionsController
from .temperature_sensor import W1TemperatureSensor
from .display_interfaces import (
    CommandLineWeateherDisplayInterface,
    LCDWeateherDisplayInterface,
    WebAppWeateherDisplayInterface,
)


def main() -> None:
    pass


# TODO argparse
if __name__ == "__main__":
    main()
