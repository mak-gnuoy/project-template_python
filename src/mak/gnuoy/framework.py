import json
import logging
import logging.config
import tomllib
from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse

class Config:
    @classmethod
    def load(cls, path: str) -> dict:
        with open(path, "rb") as f:
            return tomllib.load(f)


class Base(ABC):
    def __init__(self):
        self._logger = logging.getLogger()


class App(Base):
    settings: dict
    logger: logging.Logger

    def __init__(self, settings_filepath: str = "/app/conf/settings.toml"):
        with open(settings_filepath, "rb") as f:
            App.settings = tomllib.load(f)

        with open(App.settings["log"]["config"]["filepath"], "rb") as f:
            logging.config.dictConfig(json.load(f))
            App.logger = logging.getLogger()

        App.logger.info(
            f"settings: {json.dumps(
                App.settings, sort_keys=True, indent=4)}"
        )


class Store(Base):
    def __init__(self, url: str):
        super().__init__()
        self._url = url

    @classmethod
    def get_instance(cls, url: str):
        parsed_url = urlparse(url)
        if parsed_url.scheme.lower() == "file" or parsed_url.scheme.lower() == "":
            from mak.gnuoy.store import FileStore

            return FileStore.get_instance(url)
        else:
            raise Exception("Unsupported store type")

    @abstractmethod
    def set(self, **key_values):
        pass

    @abstractmethod
    def get(self, *keys):
        pass
