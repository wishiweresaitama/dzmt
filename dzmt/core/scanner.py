from pathlib import Path

from dzmt.constants import PROJECT_DIR
from dzmt.core.context.modification import ModificationContext
from dzmt.utils.serializers import TomlSerializer


class ModificationScanner:
    def __init__(self, path: Path):
        self._path = path
        self._modifications: list[ModificationContext] = self._scan_modifications()

    def get_modifications(self) -> list[ModificationContext]:
        return self._modifications

    def get_clientside_modifications(self) -> list[ModificationContext]:
        return [
            modification
            for modification in self._modifications
            if modification.is_clientside()
        ]

    def get_serverside_modifications(self) -> list[ModificationContext]:
        return [
            modification
            for modification in self._modifications
            if modification.is_serverside()
        ]

    def _scan_modifications(self) -> list[ModificationContext]:
        modifications = []
        for modification_path in self._path.glob("**/"):
            modification = ModificationContext(TomlSerializer(), modification_path)
            modification.validate()
            if modification.is_valid() and modification.is_enabled():
                modifications.append(modification)
        return modifications
