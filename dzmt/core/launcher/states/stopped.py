from dzmt.core.launcher.launcher import GameLauncher
from dzmt.utils.executor import ProcessExecutor

from .base import LauncherState


class StoppedState(LauncherState):
    _launcher: GameLauncher

    def __init__(self, launcher: GameLauncher):
        self._launcher = launcher

    def start(self):
        from .running import RunningState

        self._launcher.process = ProcessExecutor(
            self._launcher.executable, self._launcher.arguments
        )
        self._launcher.process.start()
        self._launcher.change_state(RunningState(self._launcher))

    def stop(self): ...
