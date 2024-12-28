import logging
from environs import Env
from typing import Optional


class Config:
    def __init__(self) -> None:
        self.env = Env()
        self.env.read_env()
        self.logging_level: Optional[int] = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        self.logging_level: int = logging.getLevelName(
            self.env.str("LOGGING_LEVEL", "INFO")
        )
        logging.basicConfig(
            level=self.logging_level,
            format="[%(asctime)s][%(levelname)s]:  %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def read_env_varaibles(self) -> None:
        self.record_data_period = self.env.int("RECORD_DATA_PERIOD", 30)  # mins
