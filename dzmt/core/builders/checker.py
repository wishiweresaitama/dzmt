from dzmt.core.context.modification import ModificationContext
from dzmt.core.providers.project import ProjectConfigProvider


class BuildChecker:
    def __init__(self, project: ProjectConfigProvider):
        self._project = project

    def perform_check(self, modification: ModificationContext):
        modification_path = (
            self._project.build.destination / modification.name / "addons"
        )
        if not modification_path.exists():
            raise FileNotFoundError(f"Modification {modification.name} was not built")

        for file in modification_path.glob("*.pbo"):
            if file.name == f"{modification.name}.pbo":
                break
        else:
            raise FileNotFoundError(f"Modification {modification.name} was not built")
