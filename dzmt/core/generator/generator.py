from abc import ABC
from pathlib import Path
from typing import Any, Callable, Dict

from dzmt.core.template.base import Template, TemplateKind, TemplateSpec


class GeneratorError(Exception):
    """Base class for generator errors."""


class InvalidTemplateError(GeneratorError):
    """Raised when a template is invalid."""


class ContentGenerator(ABC):
    def __init__(self, template: Template, path: Path):
        self._template = template
        self._path = path

    def generate(self):
        self._validate_inputs()
        for name, spec in self._template.get_template().items():
            spec = TemplateSpec(**spec)
            spec.validate()
            self._create(name, spec, self._path)

    def _validate_inputs(self):
        if not isinstance(self._template, Template):
            raise ValueError(
                f"Template must be an instance of Template, got {self._template!r}"
            )
        if not isinstance(self._path, Path):
            raise ValueError(f"Path must be a Path, got {self._path!r}")

    def _create(self, name: str, spec: TemplateSpec, path: Path):
        creator = self._get_creator(spec.kind)
        creator(name, spec.spec, path)

    def _get_creator(self, kind: str) -> Callable[[str, Dict[str, Any], Path], None]:
        creators = {
            TemplateKind.DIRECTORY.value: self._create_directory,
            TemplateKind.FILE.value: self._create_file,
        }
        return creators[kind]

    def _create_directory(self, name: str, spec: Dict[str, Any], path: Path):
        dir_path = path / name
        dir_path.mkdir(parents=True, exist_ok=True)

        for subname, subvalue in spec.items():
            subspec = TemplateSpec(**subvalue)
            subspec.validate()
            self._create(subname, subspec, dir_path)

    def _create_file(self, name: str, spec: Dict[str, Any], path: Path):
        file_path = path / name
        file_path.write_text(spec["content"] if "content" in spec else "")
