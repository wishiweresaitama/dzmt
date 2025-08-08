from abc import ABC, abstractmethod


class LauncherState(ABC):
    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...
