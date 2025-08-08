from pathlib import Path

import click

from dzmt.cli.commands.base import Command
from dzmt.constants import PROJECT_DIR
from dzmt.core.template.project import ProjectTemplate
from dzmt.models.project import Project, ProjectDefaultConfig
from dzmt.utils.console import console
from dzmt.utils.serializers import Serializer, TomlSerializer
from dzmt.utils.wizard import Wizard


class InitCommandError(Exception):
    """Base exception for the init command"""


class InitCommandValidationError(InitCommandError):
    """Validation error for the init command"""


class InitCommandExecutionError(InitCommandError):
    """Execution error for the init command"""


class InitCommand(Command):
    def __init__(self, path: Path, serializer: Serializer):
        self.path = path
        self._serializer = serializer

    def execute(self):
        try:
            self._execute()
        except (InitCommandValidationError, InitCommandExecutionError) as e:
            console.print(f"[red]{e}[/red]", style="bold")

    def _execute(self):
        self._validate_execution()
        values = self._get_user_input()
        self._create_project(values)

    def _validate_execution(self):
        if not self.path.is_dir():
            raise InitCommandValidationError(
                "Provided path is not a valid DZMT project"
            )

        if (self.path / PROJECT_DIR).exists():
            raise InitCommandValidationError("Project already initialized")

    def _get_user_input(self):
        values = {
            "name": ("Enter the name of the project", Path(self.path).name),
            "author": ("Enter the author of the project", ""),
            "version": ("Enter the version of the project", "1.0.0"),
            "description": ("Enter the description of the project", ""),
        }

        for key, value in values.items():
            values[key] = click.prompt(f"{value[0]}", default=value[1])

        return values

    def _create_project(self, values: dict):
        Wizard(
            self.path,
            ProjectTemplate(
                Project(
                    default=ProjectDefaultConfig(
                        name=values["name"],
                        author=values["author"],
                        version=values["version"],
                        description=values["description"],
                    )
                ),
                self._serializer,
            ),
        ).run()


@click.command()
@click.argument("path", type=click.Path(exists=True, resolve_path=True), default=".")
def init(path: click.Path):
    InitCommand(Path(path), TomlSerializer()).execute()
