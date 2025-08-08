from pathlib import Path

from pydantic import ValidationError

from dzmt.models.modification import (
    Modification,
    ModificationBuild,
    ModificationDetails,
    ModificationLaunch,
)
from dzmt.utils.console import console

from .base import ModuleContext


class ModificationConfigProvider:
    @property
    def build(self) -> ModificationBuild: ...

    @property
    def details(self) -> ModificationDetails: ...

    @property
    def launch(self) -> ModificationLaunch: ...

    @property
    def name(self) -> str: ...

    @property
    def path(self) -> Path: ...

    @property
    def prefix(self) -> str: ...


class ModificationContext(ModuleContext, ModificationConfigProvider):
    _modification: Modification | None = None

    def validate(self) -> None:
        try:
            super().validate()
        except ValidationError as e:
            console.print(
                f"[yellow]Invalid modification configuration in {self._path}[/yellow]",
                style="bold",
            )
            for error in e.errors():
                console.print(
                    f"[yellow]{error['loc']}: {error['msg']}[/yellow]", style="bold"
                )
        except FileNotFoundError:
            ...

    def is_enabled(self) -> bool:
        return self._modification.configuration.enabled

    def is_clientside(self) -> bool:
        return not self.is_serverside()

    def is_serverside(self) -> bool:
        return self._modification.configuration.serverside

    def _validate_path(self) -> None:
        if not self._path.is_dir():
            raise FileNotFoundError(f"{self._path} is not a valid modification")

    def _parse(self) -> None:
        file_content = self._read_config_file()
        data = self._serializer.load(file_content)
        self._modification = Modification(**data)

    def _read_config_file(self) -> str:
        with open(self._get_config_path(), "r") as config_file:
            return config_file.read()

    def _get_config_name(self) -> str:
        return f"modification.{self._get_extension()}"

    def _get_config_path(self) -> Path:
        return self._path / self._get_config_name()

    @property
    def prefix(self) -> str:
        return self._modification.prefix.replace("/", "\\")

    @property
    def name(self) -> str:
        return self._modification.name

    @property
    def path(self) -> Path:
        return self._path

    @property
    def build(self) -> ModificationBuild:
        return self._modification.configuration.build

    @property
    def details(self) -> ModificationDetails:
        return self._modification.details

    @property
    def launch(self) -> ModificationLaunch:
        return self._modification.configuration.launch

    def get_complete_details(self) -> dict:
        return {
            "name": self._modification.name,
            "author": self._modification.author,
            **self.details.model_dump(by_alias=True),
        }
