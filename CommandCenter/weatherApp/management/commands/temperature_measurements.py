from django.core.management.base import BaseCommand
from weatherApp.logic.controller import WeatherConditionsMainLogic
import time


class Command(BaseCommand):
    """
    Class responsible for starting temperature measurement for weatherApp and proper display it.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.measurement_thread: threading.Thread | None = None

    help = "Command responsible for starting and stopping temperature measurement for weatherApp and properly display measurements"
    _is_measurement_running = False

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--displays",
            nargs="*",
            type=str,
            help="""Add multiple ways of display temperture. Default way is to display it by django weatherApp. 
                            You can add additional ways by passing:
                            - 'cmd' for command line output,
                            - 'lcd' for lcd external display.
                            Example usage for all display ways: 
                            `python3 manage.py temperature_measurements --displays cmd lcd`""",
        )

        # parser.add_argument("--stop", action='store_true', help="Stops temperature measurements")

    def handle(self, *args, **kwargs) -> None:
        # if kwargs["stop"]:
        #     if not self._is_measurement_running:
        #         self.stdout.write(
        #         self.style.WARNING('Cannot stop measurement because it is not running')
        #         )
        #         return

        #     self.stdout.write(
        #         self.style.SUCCESS('Succesfully stopped measurement!')
        #         )
        #     return
        self._is_measurement_running = True
        self.measurement_thread = WeatherConditionsMainLogic(kwargs["displays"])
        self.measurement_thread.start()
        self.stdout.write(self.style.SUCCESS("Succesfully started measurement!"))
        try:
            while self._is_measurement_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stderr.write("Keyboard interrupt caught!. Stopping measurement!")
        finally:
            self._is_measurement_running = False
            self.measurement_thread.stop()
            self.measurement_thread.join()
