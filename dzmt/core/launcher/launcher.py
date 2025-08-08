from abc import ABC, abstractmethod
from pathlib import Path

import keyboard

from dzmt.core.context.project import ProjectContext
from dzmt.models.project import LauncherExecutableConfig
from dzmt.utils.executor import ProcessExecutor

from .logreader import LogReader
from .states import LauncherState


class GameLauncher(ABC):
    _project: ProjectContext
    _state: LauncherState
    _process: ProcessExecutor

    def __init__(self, project: ProjectContext, reader: LogReader):
        self._project = project
        self._reader = reader
        for hotkey in self._get_executable_config().hotkeys.execute:
            self._add_execute_hotkey(hotkey)
        for hotkey in self._get_executable_config().hotkeys.terminate:
            self._add_terminate_hotkey(hotkey)
        self._initialize_state()

    def _initialize_state(self):
        from .states.stopped import StoppedState

        self._state = StoppedState(self)

    @property
    def label(self) -> str: ...

    @property
    def profile(self) -> Path:
        return self._project.launcher.replica / Path(
            self._get_executable_config().profile
        )

    @property
    def executable(self) -> Path:
        return self._project.launcher.replica / self._project.launcher.executable

    @property
    def arguments(self) -> list[str]:
        return self._get_prepared_arguments()

    @property
    def process(self) -> ProcessExecutor:
        return self._process

    @process.setter
    def process(self, process: ProcessExecutor):
        self._process = process

    def change_state(self, state: LauncherState):
        self._state = state

    def terminate(self):
        self._stop()

    def push_log(self, log: Path):
        self._reader.push_log(log, self.label)

    def pop_log(self, log: Path):
        self._reader.pop_log(log)

    def _add_execute_hotkey(self, hotkey: str):
        keyboard.add_hotkey(hotkey, self._start)

    def _add_terminate_hotkey(self, hotkey: str):
        keyboard.add_hotkey(hotkey, self._stop)

    def _start(self):
        self._state.start()

    def _stop(self):
        self._state.stop()

    @abstractmethod
    def _get_executable_config(self) -> LauncherExecutableConfig: ...

    def _get_prepared_arguments(self) -> list[str]:
        return self._get_executable_config().arguments + [
            f"-profiles={self._get_profile_argument()}",
            "-mod="
            + ";".join([self._get_clientside_mods(), self._get_workshop_mods()]),
        ]

    def _get_profile_argument(self) -> str:
        return self._get_executable_config().profile.replace("/", "\\")

    def _get_clientside_mods(self) -> str:
        modifications = self._project.get_clientside_modifications()
        return ";".join(
            [
                self._project.get_modification_build_path(modification).as_posix()
                for modification in modifications
            ]
        )

    def _get_workshop_mods(self) -> str:
        modifications = self._project.get_clientside_workshop_modifications()
        return ";".join([modification.as_posix() for modification in modifications])


class ServerLauncher(GameLauncher):
    def _get_executable_config(self) -> LauncherExecutableConfig:
        return self._project.server

    def _get_prepared_arguments(self) -> list[str]:
        return super()._get_prepared_arguments() + [
            "-servermod="
            + ";".join(
                [self._get_serverside_mods(), self._get_serverside_workshop_mods()]
            ),
        ]

    def _get_serverside_mods(self) -> str:
        modifications = self._project.get_serverside_modifications()
        return ";".join(
            [
                self._project.get_modification_build_path(modification).as_posix()
                for modification in modifications
            ]
        )

    def _get_serverside_workshop_mods(self) -> str:
        return ";".join(
            [
                modification.as_posix()
                for modification in self._project.get_serverside_workshop_modifications()
            ]
        )

    @property
    def label(self) -> str:
        return "Server"


class ClientLauncher(GameLauncher):
    def _get_executable_config(self) -> LauncherExecutableConfig:
        return self._project.client

    @property
    def label(self) -> str:
        return "Client"
