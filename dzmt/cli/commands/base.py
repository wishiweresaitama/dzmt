from abc import ABC, abstractmethod

from pydantic import ValidationError

from dzmt.core.context.project import ProjectContext
from dzmt.utils.console import console


class Command(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @abstractmethod
    def execute(self):
        pass


class ProjectCommand(Command):
    def __init__(self, project: ProjectContext):
        self._project = project
