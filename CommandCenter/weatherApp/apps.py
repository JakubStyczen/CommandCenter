from django.apps import AppConfig
from CommandCenter.config import Config
from dotenv import load_dotenv


class WeatherappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "weatherApp"

    def ready(self) -> None:
        load_dotenv()
        Config().setup_logging()
