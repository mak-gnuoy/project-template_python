from abc import abstractmethod
import json
import os
from pathlib import Path
from urllib.parse import urlparse, unquote

from mak.gnuoy.framework import Base


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


class FileStore(Store):
    def __init__(self, path: str):
        super().__init__(path)

        parsed = urlparse(path)
        if parsed.scheme.lower() == "file" or parsed.scheme.lower() == "":
            self._path = path
        else:
            raise Exception("path is not matched with FileStore")


class JsonFileStore(FileStore):
    def __init__(self, path: str):
        super().__init__(path)

        parsed_url = urlparse(path)
        if parsed_url.scheme.lower() == "file" or parsed_url.scheme.lower() == "":
            if Path(parsed_url.path).suffix.lower() == ".json":
                path = os.path.abspath(
                    os.path.join(parsed_url.netloc, unquote(parsed_url.path))
                )
                super().__init__(path)
            else:
                raise Exception("path is not matched with JsonFileStore")
        else:
            raise Exception("Unsupported store type")

    def set(self, **key_values) -> dict:
        try:
            with open(self._path, "r") as f:
                file_data = json.load(f)
        except FileNotFoundError as e:
            os.makedirs(os.path.dirname(self._path), exist_ok=True)
            file_data = dict()

        file_data.update(key_values)

        with open(self._path, "w") as f:
            json.dump(file_data, f)
            self._logger.debug(f"{key_values} written to the {self._path}")

        return file_data

    def get(self, *keys) -> dict:
        with open(self._path, "r") as f:
            file_data = json.load(f)

        selected_data = dict()
        for key_in_file_data in file_data.keys():
            for key in keys:
                if key == key_in_file_data:
                    selected_data[key_in_file_data] = file_data[key_in_file_data]
        self._logger.debug(f"{selected_data} read from the {self._path}")

        return selected_data

    def get_value(self, key: str):
        with open(self._path, "r") as f:
            file_data = json.load(f)
        self._logger.debug(f"{key}: {file_data[key]} read from the {self._path}")

        return file_data[key]
