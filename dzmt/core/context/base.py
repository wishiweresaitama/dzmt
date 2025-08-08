from abc import ABC, abstractmethod
from pathlib import Path

from dzmt.utils.serializers import Serializer


class ModuleContext(ABC):
    _is_valid: bool = False

    def __init__(self, serializer: Serializer, path: Path):
        self._serializer = serializer
        self._path = path.resolve()

    def is_valid(self) -> bool:
        return self._is_valid

    def get_serializer(self) -> Serializer:
        return self._serializer

    def get_path(self) -> Path:
        return self._path

    def validate(self) -> None:
        self._validate_path()
        self._parse()
        self._initialize()

    def _initialize(self) -> None:
        self._is_valid = True

    @abstractmethod
    def _validate_path(self) -> None: ...

    @abstractmethod
    def _parse(self) -> None: ...

    def _get_extension(self) -> str:
        return self._serializer.extension
