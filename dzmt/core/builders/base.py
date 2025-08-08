from abc import ABC, abstractmethod
from pathlib import Path

from dzmt.core.context.modification import ModificationContext


class Builder(ABC):
    def build(self, modification: ModificationContext, destination: Path):
        self._pre_build(modification, destination)
        self._build(modification, destination)
        self._post_build(modification, destination)

    def _pre_build(self, modification: ModificationContext, destination: Path):
        destination.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def _build(self, modification: ModificationContext, destination: Path): ...

    def _post_build(self, modification: ModificationContext, destination: Path): ...
