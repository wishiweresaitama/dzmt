from dzmt.cli.commands.build.selector import Selector
from dzmt.core.context.modification import ModificationContext
from dzmt.core.context.project import ProjectContext


class SelectorFactory:
    _registry: dict[str, type[Selector]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(selector_cls: type[Selector]):
            cls._registry[name] = selector_cls
            return selector_cls

        return wrapper

    @classmethod
    def create(cls, name: str, project: ProjectContext) -> Selector:
        return cls._registry[name](project)


@SelectorFactory.register("full")
class FullSelector(Selector):
    def get_modifications(self) -> list[ModificationContext]:
        return self._project.get_modifications()


@SelectorFactory.register("client")
class ClientSelector(Selector):
    def get_modifications(self) -> list[ModificationContext]:
        return self._project.get_clientside_modifications()


@SelectorFactory.register("server")
class ServerSelector(Selector):
    def get_modifications(self) -> list[ModificationContext]:
        return self._project.get_serverside_modifications()
