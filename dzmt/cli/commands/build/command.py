from pathlib import Path

import click

from dzmt.cli.commands.base import ProjectCommand
from dzmt.core.builders.base import Builder
from dzmt.core.builders.builders import BuilderFactory
from dzmt.core.context.modification import ModificationContext
from dzmt.core.context.project import ProjectContext
from dzmt.utils.serializers import TomlSerializer

from .factory import SelectorFactory
from .selector import Selector


class BuildCommand(ProjectCommand):
    _builder: Builder | None = None
    _selector: Selector | None = None

    def __init__(self, project: ProjectContext, builder: Builder, selector: Selector):
        super().__init__(project)
        self._builder = builder
        self._selector = selector

    def execute(self):
        modifications = self._get_modifications()

        for modification in modifications:
            self._builder.build(
                modification, self._project.get_modification_build_path(modification)
            )

    def _get_modifications(self) -> list[ModificationContext]:
        return self._selector.get_modifications()


@click.command()
@click.option("--full", "build", flag_value="full", default=True)
@click.option("--client-only", "build", flag_value="client")
@click.option("--server-only", "build", flag_value="server")
def build(build: str):
    project = ProjectContext(TomlSerializer(), Path.cwd())
    project.validate(exit_on_error=True)
    command = BuildCommand(
        project,
        BuilderFactory.create(project.build.builder),
        SelectorFactory.create(build, project),
    )
    command.execute()
