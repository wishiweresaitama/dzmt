from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class TemplateKind(Enum):
    DIRECTORY = "directory"
    FILE = "file"


class TemplateError(Exception):
    """Base exception for template errors."""


class InvalidTemplateError(TemplateError):
    """Error raised when an invalid template is encountered."""


class InvalidTemplateKindError(TemplateError):
    """Error raised when an invalid template kind is encountered."""


class InvalidTemplateSpecError(TemplateError):
    """Error raised when an invalid template spec is encountered."""


@dataclass
class TemplateSpec:
    kind: str
    spec: Dict[str, Any]

    def validate(self) -> None:
        if not isinstance(self.kind, str):
            raise InvalidTemplateSpecError(f"Kind must be a string, got {self.kind!r}")

        if not isinstance(self.spec, dict):
            raise InvalidTemplateSpecError(
                f"Spec must be a dictionary, got {self.spec!r}"
            )

        if self.kind not in {kind.value for kind in TemplateKind}:
            raise InvalidTemplateSpecError(f"Invalid template kind: {self.kind!r}")


class Template(ABC):
    def __init__(self): ...

    @abstractmethod
    def get_template(self): ...
