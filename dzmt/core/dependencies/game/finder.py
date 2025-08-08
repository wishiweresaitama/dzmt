from pathlib import Path

from dzmt import settings


class RegistryError(Exception):
    """Exception raised when there are issues accessing the Windows registry."""


class PathError(Exception):
    """Exception raised when the game path is invalid or not found."""


class GameSeeker:
    """Configuration settings for the DayZ game."""

    @property
    def path(self) -> Path:
        path = (
            Path(settings.DAYZ_GAME_DIR)
            if settings.DAYZ_GAME_DIR
            else self._find_registry()
        )
        self._validate_directory(path)
        return path

    def _find_registry(self) -> Path:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Bohemia Interactive\dayz"
        )
        path = winreg.QueryValueEx(key, "main")[0]
        winreg.CloseKey(key)
        return Path(path)

    def _validate_directory(self, path: Path) -> None:
        if not path.exists():
            raise PathError(f"Game path does not exist: {path}")

        required_files = ["DayZ_x64.exe"]
        for file in required_files:
            if not (path / file).exists():
                raise PathError(f"Required game file not found: {file}")
