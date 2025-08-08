import importlib.resources as pkg_resources
import subprocess
import tempfile
from pathlib import Path

from dzmt.core.context.modification import ModificationContext
from dzmt.utils.console import console
from dzmt.utils.serializers import PropertiesSerializer

from .base import Builder


class BuilderFactory:
    _registry: dict[str, type[Builder]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(builder_cls: type[Builder]):
            cls._registry[name] = builder_cls
            return builder_cls

        return wrapper

    @classmethod
    def create(cls, name: str) -> Builder:
        return cls._registry[name]()

    @classmethod
    def get_builders(cls) -> list[str]:
        return list(cls._registry.keys())


class MockBuilder(Builder):
    def _pre_build(self, modification: ModificationContext):
        console.print(f"[blue]Pre-building modification {modification.name}[/blue]")

    def _build(self, modification: ModificationContext):
        console.print(f"[green]Building modification {modification.name}[/green]")

    def _post_build(self, modification: ModificationContext):
        console.print(f"[green]Post-building modification {modification.name}[/green]")


@BuilderFactory.register("addonbuilder")
class AddonBuilder(Builder):
    def _build(self, modification: ModificationContext, destination: Path):
        package = pkg_resources.files("tools")
        executable = package / "bin" / "addonbuilder" / "AddonBuilder.exe"
        if not executable.exists():
            raise FileNotFoundError(f"AddonBuilder.exe not found at {executable}")

        console.print(f"[green]Building modification {modification.name}[/green]")

        with tempfile.TemporaryDirectory() as temp_dir:
            wildcard = Path(temp_dir, "wildcard.txt")
            with open(wildcard, "w") as f:
                f.write(",".join(modification.build.include))

            command = [
                executable.name,
                str(modification.path),
                str(Path(destination / "addons")),
                "-toolsDirectory=" + str(package),
                "-prefix=" + modification.prefix,
                "-temp=" + str(Path(temp_dir, modification.name)),
                "-include=" + str(wildcard),
                "-clear",
                "-packonly",
            ]

            try:
                subprocess.run(
                    command,
                    cwd=executable.parent,
                    shell=True,
                    check=True,
                )
                console.print(f"[green]Built modification {modification.name}[/green]")
            except subprocess.CalledProcessError:
                console.print(
                    f"[red]Failed to build modification {modification.name}[/red]"
                )

    def _post_build(self, modification: ModificationContext, destination: Path):
        with open(destination / "mod.cpp", "w") as f:
            content = PropertiesSerializer().dump(modification.get_complete_details())
            f.write(content)
