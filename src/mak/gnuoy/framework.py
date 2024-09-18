import json
import logging
import logging.config
import tomllib
from abc import ABC, abstractmethod

with open("/app/conf/settings.toml", "rb") as f:
    settings = tomllib.load(f)

with open(settings["log"]["config"]["filepath"], "rb") as f:
    logging.config.dictConfig(json.load(f))

logger = logging.getLogger(__name__)


class Config:
    @classmethod
    def load(cls, path: str) -> dict:
        with open(path, "rb") as f:
            return tomllib.load(f)


class Base(ABC):
    def __init__(self):
        self._logger = logger


class App(Base):
    def __init__(self):
        self.settings = settings
        self.logger = logger

        self.logger.info(
            f"settings: {json.dumps(
                self.settings, sort_keys=True, indent=4)}"
        )


class Store(Base):
    def __init__(self, url: str):
        super().__init__()
        self._url = url

    @abstractmethod
    def set(self, **key_values):
        pass

    @abstractmethod
    def get(self, *keys):
        pass
