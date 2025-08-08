import _winapi as win32
import hashlib
import shutil
from pathlib import Path

from dzmt.core.context.project import ProjectConfigProvider
from dzmt.core.dependencies.game.finder import GameSeeker
from dzmt.utils.console import console

from .constants import DAYZ_REPLICA_STRUCTURE


class GameReplica:
    _config: ProjectConfigProvider

    def __init__(self, config: ProjectConfigProvider):
        self._config = config

    def update(self) -> None:
        self._retrieve_game_path()
        self._validate_path()
        self._update_folders()
        self._update_files()
        self._update_executable()

    def _retrieve_game_path(self) -> None:
        self._game_path = GameSeeker().path

    def _sync_file(self, source: Path, destignation: Path) -> None:
        if not source.exists():
            raise FileNotFoundError(f"Source file {source} does not exist")

        if not destignation.exists() or not self._compare_files(source, destignation):
            shutil.copyfile(source, destignation)
            console.print(f"[green]Synced file {source} <=> {destignation}[/green]")

    def _validate_path(self) -> None:
        if not self._game_path.exists():
            raise FileNotFoundError(f"Game path {self._game_path} does not exist")

        self._config.launcher.replica.mkdir(parents=True, exist_ok=True)

    def _update_folders(self) -> None:
        for folder in DAYZ_REPLICA_STRUCTURE["folders"]:
            source = self._game_path / folder
            destignation = self._config.launcher.replica / folder

            try:
                win32.CreateJunction(
                    str(source),
                    str(destignation),
                )
                console.print(
                    f"[green]Created junction {source} <=> {destignation}[/green]"
                )
            except FileExistsError:
                pass

    def _update_files(self) -> None:
        for file in DAYZ_REPLICA_STRUCTURE["files"]:
            source = self._game_path / file
            destignation = self._config.launcher.replica / file
            self._sync_file(source, destignation)

    def _update_executable(self) -> None:
        self._sync_file(
            self._game_path / self._config.launcher.executable,
            self._config.launcher.replica / self._config.launcher.executable,
        )

    def _compare_files(self, first: Path, second: Path) -> bool:
        return (
            hashlib.md5(first.read_bytes()).hexdigest()
            == hashlib.md5(second.read_bytes()).hexdigest()
        )
