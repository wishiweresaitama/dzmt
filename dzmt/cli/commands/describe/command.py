from pathlib import Path

import click

from dzmt.cli.commands.base import ProjectCommand
from dzmt.core.context.project import ProjectContext
from dzmt.utils.console import console
from dzmt.utils.serializers import TomlSerializer


class DescribeCommand(ProjectCommand):
    def execute(self):
        console.print(self._project)


@click.command()
def describe():
    project = ProjectContext(TomlSerializer(), Path.cwd())
    project.validate(exit_on_error=True)
    DescribeCommand(project).execute()
