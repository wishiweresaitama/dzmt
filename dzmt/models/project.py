from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field, field_serializer, field_validator

from dzmt.constants import LAUNCHER_EXECUTABLE
from dzmt.core.builders.builders import BuilderFactory


class ProjectDefaultConfig(BaseModel):
    name: str
    author: str
    version: str
    description: str


class LauncherHotkeysConfig(BaseModel):
    execute: List[str] = Field(default_factory=list)
    terminate: List[str] = Field(default_factory=list)


class LauncherExecutableConfig(BaseModel):
    hotkeys: LauncherHotkeysConfig = Field(default_factory=LauncherHotkeysConfig)
    arguments: List[str] = Field(default_factory=list)
    profile: str = Field(default="")


class ProjectLauncherConfig(BaseModel):
    replica: Path = Field(default=Path(".dzmt/replica"))
    executable: str = LAUNCHER_EXECUTABLE
    client: Optional[LauncherExecutableConfig] = None
    server: Optional[LauncherExecutableConfig] = None

    @field_validator("replica")
    def validate_path(cls, v):
        return Path(v).resolve()

    @field_serializer("replica")
    def serialize_path(self, v: Path) -> str:
        return v.as_posix()


class ProjectBuilderConfig(BaseModel):
    destination: Path = Field(default=Path(".dzmt/dist"))
    builder: str = Field(default="addonbuilder")

    @field_validator("destination")
    def validate_path(cls, v):
        return v.resolve()

    @field_serializer("destination")
    def serialize_path(self, v: Path) -> str:
        return v.as_posix()

    @field_validator("builder")
    def validate_builder(cls, v):
        if v not in BuilderFactory.get_builders():
            raise ValueError(
                f"Builder {v} is invalid, valid builders: {BuilderFactory.get_builders()}"
            )
        return v


class WorkshopModification(BaseModel):
    path: Path

    @field_validator("path")
    def validate_path(cls, v):
        return Path(v).resolve()

    @field_serializer("path")
    def serialize_path(self, v: Path) -> str:
        return v.as_posix()


class WorkshopModificationConfig(BaseModel):
    modifications: List[WorkshopModification] = Field(default=[])


class WorkshopConfig(BaseModel):
    client: WorkshopModificationConfig = Field(
        default_factory=WorkshopModificationConfig
    )
    server: WorkshopModificationConfig = Field(
        default_factory=WorkshopModificationConfig
    )


class Project(BaseModel):
    default: ProjectDefaultConfig
    launcher: ProjectLauncherConfig = Field(default_factory=ProjectLauncherConfig)
    build: ProjectBuilderConfig = Field(default_factory=ProjectBuilderConfig)
    workshop: WorkshopConfig = Field(default_factory=WorkshopConfig)
