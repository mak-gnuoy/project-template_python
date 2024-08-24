import json
import os
from pathlib import Path
from urllib.parse import urlparse, unquote

from mak.gnuoy.framework import Store


class FileStore(Store):
    def __init__(self, path: str):
        parsed = urlparse(path)
        if parsed.scheme.lower() == "file" or parsed.scheme.lower() == "":
            self._path = path
        else:
            raise Exception("path is not matched with FileStore")

    @classmethod
    def get_instance(cls, url: str):
        parsed_url = urlparse(url)
        if parsed_url.scheme.lower() == "file" or parsed_url.scheme.lower() == "":
            if Path(parsed_url.path).suffix.lower() == ".json":
                from mak.gnuoy.store import JsonFileStore

                return JsonFileStore(url)
            else:
                raise Exception("Unsupported store type")
        else:
            raise Exception("Unsupported store type")


class JsonFileStore(FileStore):
    def __init__(self, path: str):
        parsed = urlparse(path)
        if Path(parsed.path).suffix.lower() == ".json":
            path = os.path.abspath(os.path.join(parsed.netloc, unquote(parsed.path)))
            super().__init__(path)
        else:
            raise Exception("file_path is not matched with JsonFileStore")

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

        return file_data

    def get(self, *keys) -> dict:
        try:
            with open(self._path, "r") as f:
                file_data = json.load(f)
        except FileNotFoundError as e:
            file_data = dict()

        if len(keys) <= 0:
            return file_data

        selected_data = dict()
        for key_in_file_data in file_data.keys():
            for key in keys:
                if key == key_in_file_data:
                    selected_data[key_in_file_data] = file_data[key_in_file_data]
        return selected_data
