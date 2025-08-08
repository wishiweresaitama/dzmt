import json
from abc import ABC, abstractmethod

import toml


class SerializationError(Exception):
    """Base class for all serialization errors."""


class Serializer(ABC):
    extension: str

    @abstractmethod
    def dump(self, data: dict) -> str: ...

    @abstractmethod
    def load(self, data: str) -> dict: ...


class JsonSerializer(Serializer):
    extension: str = "json"

    def dump(self, data: dict) -> str:
        try:
            return json.dumps(data)
        except TypeError as e:
            raise SerializationError(f"Invalid type: {e}")

    def load(self, data: str) -> dict:
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise SerializationError(f"Invalid JSON: {e.msg}")


class TomlSerializer(Serializer):
    extension: str = "toml"

    def dump(self, data: dict) -> str:
        try:
            return toml.dumps(data)
        except TypeError as e:
            raise SerializationError(f"Invalid type: {e}")

    def load(self, data: str) -> dict:
        try:
            return toml.loads(data)
        except toml.TomlDecodeError as e:
            raise SerializationError(f"Invalid TOML: {e.msg}")


class PropertiesSerializer(Serializer):
    extension: str = "cpp"

    def dump(self, data: dict) -> str:
        return "\n".join([f'{k} = "{v}";' for k, v in data.items()])

    def load(self, data: str) -> dict:
        return {
            line.split("=")[0]: line.split("=")[1].strip('"')
            for line in data.split("\n")
            if "=" in line
        }
