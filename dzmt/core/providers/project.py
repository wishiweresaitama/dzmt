from dzmt.models.project import (
    LauncherExecutableConfig,
    ProjectBuilderConfig,
    ProjectDefaultConfig,
    ProjectLauncherConfig,
)


class ProjectConfigProvider:
    @property
    def server(self) -> LauncherExecutableConfig: ...

    @property
    def client(self) -> LauncherExecutableConfig: ...

    @property
    def launcher(self) -> ProjectLauncherConfig: ...

    @property
    def default(self) -> ProjectDefaultConfig: ...

    @property
    def build(self) -> ProjectBuilderConfig: ...
