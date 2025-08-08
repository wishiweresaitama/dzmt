from pathlib import Path

import click

from dzmt.cli.commands.base import ProjectCommand
from dzmt.core.builders.builders import BuilderFactory
from dzmt.core.builders.checker import BuildChecker
from dzmt.core.context.project import ProjectContext
from dzmt.core.launcher.launcher import ClientLauncher, ServerLauncher
from dzmt.core.launcher.logreader import LogReader
from dzmt.core.launcher.patcher import ModificationPatcher
from dzmt.core.launcher.replica import GameReplica
from dzmt.utils.console import console
from dzmt.utils.helpers import run_interrupt_listener
from dzmt.utils.serializers import TomlSerializer


class LaunchCommand(ProjectCommand):
    def execute(self) -> None:
        self._validate_configuration()
        self._create_game_replica()
        self._validate_build()
        self._patch_modifications()
        self._run_handlers()

    def _validate_configuration(self) -> None:
        command_interrupt = False
        if not self._project.launcher.client:
            console.print(
                "[red]Client launcher configuration is missing[/red]",
                style="bold",
            )
            command_interrupt = True

        if not self._project.launcher.server:
            console.print(
                "[red]Server launcher configuration is missing[/red]",
                style="bold",
            )
            command_interrupt = True

        if command_interrupt:
            exit(1)

    def _create_game_replica(self) -> None:
        replica = GameReplica(self._project)
        try:
            replica.update()
        except Exception as e:
            console.print(
                f"[red]{e}[/red]",
                style="bold",
            )
            exit(1)

    def _run_handlers(self) -> None:
        reader = LogReader()
        self._server_launcher = ServerLauncher(self._project, reader)
        self._client_launcher = ClientLauncher(self._project, reader)

        run_interrupt_listener()

        self._server_launcher.terminate()
        self._client_launcher.terminate()
        reader.join()

    def _validate_build(self) -> None:
        checker = BuildChecker(self._project)
        for modification in self._project.get_modifications():
            try:
                checker.perform_check(modification)
            except FileNotFoundError:
                console.print(
                    f"[yellow]Modification {modification.name} has no any build, building...[/yellow]",
                    style="bold",
                )
                BuilderFactory.create(self._project.build.builder).build(
                    modification,
                    self._project.get_modification_build_path(modification),
                )

    def _patch_modifications(self) -> None:
        for modification in self._project.get_modifications():
            if modification.launch.patching:
                ModificationPatcher(modification, self._project).patch()
            else:
                ModificationPatcher(modification, self._project).unpatch()


@click.command()
def launch():
    project = ProjectContext(TomlSerializer(), Path.cwd())
    project.validate(exit_on_error=True)
    LaunchCommand(project).execute()
