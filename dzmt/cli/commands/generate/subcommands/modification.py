from pathlib import Path

import click

from dzmt.cli.commands.base import ProjectCommand
from dzmt.core.context.project import ProjectContext
from dzmt.core.template.modification import ModificationTemplate
from dzmt.models.modification import Modification
from dzmt.utils.console import console
from dzmt.utils.serializers import TomlSerializer
from dzmt.utils.wizard import Wizard


class ModificationCommandError(Exception):
    """Base exception for the modification command"""


class ModificationCommand(ProjectCommand):
    def __init__(self, project: ProjectContext, name: str, path: Path):
        super().__init__(project)
        self.name = name
        self.path = path

    def execute(self):
        try:
            self._execute()
        except ModificationCommandError as e:
            console.print(f"[red]{e}[/red]", style="bold")

    def _execute(self):
        self._validate_execution()
        values = self._get_user_input()
        self._create_modification(values)

    def _validate_execution(self):
        if self._project.get_modification(self.name):
            raise ModificationCommandError(f"Modification {self.name} already exists")
        elif self._get_modification_path().exists():
            raise ModificationCommandError(
                f"Path {self._get_modification_path()} already exists"
            )

    def _get_user_input(self):
        values = {
            "name": ("Enter the full name of the modification", self.name),
            "prefix": ("Enter the prefix of the modification", self.name),
            "author": ("Enter the author of the modification", ""),
        }

        for key, value in values.items():
            values[key] = click.prompt(f"{value[0]}", default=value[1])

        return values

    def _create_modification(self, values: dict):
        Wizard(
            self._get_modification_path(),
            ModificationTemplate(
                Modification(
                    name=values["name"],
                    prefix=values["prefix"],
                    author=values["author"],
                ),
                self._project.get_serializer(),
            ),
        ).run()

        console.print(
            f"[green]Modification {self.name} created successfully[/green]",
            style="bold",
        )

    def _get_modification_path(self):
        return self.path / self.name


@click.command()
@click.argument("path", type=click.Path(exists=True, resolve_path=True), default=".")
@click.option("--name", type=str, help="The name of the modification", required=True)
def modification(path: click.Path, name: str):
    project = ProjectContext(TomlSerializer(), Path.cwd())
    project.validate(exit_on_error=True)
    ModificationCommand(project, name, Path(path)).execute()
