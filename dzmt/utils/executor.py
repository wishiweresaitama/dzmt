import subprocess
from pathlib import Path
from typing import List


class ProcessExecutor:
    _process: subprocess.Popen | None = None

    def __init__(self, executable: Path, args: List[str]):
        self.executable = executable
        self.args = args

    def start(self):
        self._process = subprocess.Popen(
            " ".join([self.executable.as_posix()] + self.args),
            cwd=self.executable.parent,
        )

    def stop(self):
        self._process.kill()
