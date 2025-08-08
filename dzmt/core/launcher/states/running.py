import threading
import time
from io import TextIOWrapper

from dzmt.core.launcher.launcher import GameLauncher

from .base import LauncherState


class RunningState(LauncherState):
    _launcher: GameLauncher
    _logfile: TextIOWrapper | None = None

    def __init__(self, launcher: GameLauncher):
        self._launcher = launcher
        self._start_seeker()

    def start(self): ...

    def stop(self):
        from .stopped import StoppedState

        self._stop_seeker()
        self._launcher.process.stop()
        self._launcher.change_state(StoppedState(self._launcher))

    def _start_seeker(self):
        self._is_running = True
        self._launch_timestamp = time.time()
        self._seeker = threading.Thread(target=self._seek_logs)
        self._seeker.start()

    def _stop_seeker(self):
        self._is_running = False
        self._seeker.join()
        if self._logfile:
            self._launcher.pop_log(self._logfile)
            self._logfile.close()

    def _seek_logs(self):
        while self._is_running:
            if log_path := self._find_latest_log():
                self._logfile = open(log_path, "r")
                self._launcher.push_log(self._logfile)
                break
            time.sleep(1)

    def _find_latest_log(self):
        for log in self._launcher.profile.glob("script_*.log"):
            if log.stat().st_mtime > self._launch_timestamp:
                return log
        return None
