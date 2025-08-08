from pathlib import Path

from dzmt.core.context.modification import ModificationConfigProvider
from dzmt.core.providers.project import ProjectConfigProvider
from dzmt.utils.console import console


class ModificationPatcher:
    def __init__(
        self, modification: ModificationConfigProvider, project: ProjectConfigProvider
    ):
        self._modification = modification
        self._project = project

    def patch(self) -> None:
        import _winapi as winapi

        destination = Path(self._project.launcher.replica / self._modification.prefix)
        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            winapi.CreateJunction(
                self._modification.path.as_posix(),
                destination.as_posix(),
            )
            console.print(
                f"[green]Modification {self._modification.name} patched successfully[/green]",
                style="bold",
            )
        except FileExistsError:
            ...

    def unpatch(self) -> None:
        try:
            Path(self._project.launcher.replica / self._modification.prefix).unlink()
            console.print(
                f"[green]Modification {self._modification.name} unpatched successfully[/green]",
                style="bold",
            )
        except FileNotFoundError:
            ...
