from abc import abstractmethod

from dzmt.core.context.modification import ModificationContext
from dzmt.core.context.project import ProjectContext


class Selector:
    def __init__(self, project: ProjectContext):
        self._project = project

    @abstractmethod
    def get_modifications(self) -> list[ModificationContext]: ...
