from pathlib import Path

from pydantic import ValidationError

from dzmt.constants import PROJECT_DIR
from dzmt.core.context.modification import ModificationContext
from dzmt.core.providers.project import ProjectConfigProvider
from dzmt.core.scanner import ModificationScanner
from dzmt.models.project import (
    LauncherExecutableConfig,
    Project,
    ProjectBuilderConfig,
    ProjectDefaultConfig,
    ProjectLauncherConfig,
)
from dzmt.utils.console import console
from dzmt.utils.serializers import Serializer

from .base import ModuleContext


class ProjectContext(ModuleContext, ProjectConfigProvider):
    _project: Project | None = None
    _scanner: ModificationScanner | None = None

    def __init__(self, serializer: Serializer, path: Path):
        super().__init__(serializer, path)
        self._scanner = ModificationScanner(self._path)

    @property
    def server(self) -> LauncherExecutableConfig:
        return self._project.launcher.server

    @property
    def client(self) -> LauncherExecutableConfig:
        return self._project.launcher.client

    @property
    def launcher(self) -> ProjectLauncherConfig:
        return self._project.launcher

    @property
    def default(self) -> ProjectDefaultConfig:
        return self._project.default

    @property
    def build(self) -> ProjectBuilderConfig:
        return self._project.build

    def validate(self, exit_on_error: bool = False) -> None:
        try:
            super().validate()
        except ValidationError as e:
            console.print("[red]Failed to initialize project[/red]", style="bold")
            for error in e.errors():
                console.print(
                    f"[red]{error['loc']}: {error['msg']}[/red]", style="bold"
                )
            if exit_on_error:
                exit(1)
        except Exception as e:
            console.print(f"[red]{e}[/red]", style="bold")
            if exit_on_error:
                exit(1)

        console.print(
            f"[green]Project [bold]{self.default.name}[/bold] loaded successfully[/green]",
        )

    def get_modification(self, name: str) -> ModificationContext | None:
        for modification in self.get_modifications():
            if modification.name == name:
                return modification
        return None

    def get_modifications(self) -> list[ModificationContext]:
        return self._scanner.get_modifications()

    def get_serverside_modifications(self) -> list[ModificationContext]:
        return self._scanner.get_serverside_modifications()

    def get_serverside_workshop_modifications(self) -> list[str]:
        return [
            modification.path
            for modification in self._project.workshop.server.modifications
        ]

    def get_clientside_modifications(self) -> list[ModificationContext]:
        return self._scanner.get_clientside_modifications()

    def get_clientside_workshop_modifications(self) -> list[str]:
        return [
            modification.path
            for modification in self._project.workshop.client.modifications
        ]

    def get_modification_build_path(self, modification: ModificationContext) -> Path:
        return self.build.destination / modification.name

    def __str__(self) -> str:
        return str(self._project.model_dump())

    def _validate_path(self) -> None:
        if not self._path.is_dir() or not self._get_config_path().exists():
            raise FileNotFoundError(f"{self._path} is not a valid project")

    def _read_config_file(self) -> str:
        with open(self._get_config_path(), "r") as config_file:
            return config_file.read()

    def _parse(self) -> None:
        file_content = self._read_config_file()
        data = self._serializer.load(file_content)
        self._project = Project(**data)

    def _get_config_name(self) -> str:
        return f"project.{self._get_extension()}"

    def _get_config_path(self) -> Path:
        return self._path / PROJECT_DIR / self._get_config_name()
