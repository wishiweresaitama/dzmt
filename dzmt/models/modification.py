from pydantic import BaseModel, Field

from dzmt.constants import MODIFICATION_BUILD_INCLUDE_FILES


class ModificationDetails(BaseModel):
    action: str = Field(default="")
    author_id: str = Field(default="", alias="authorID")
    logo: str = Field(default="")
    logo_over: str = Field(default="", alias="logoOver")
    logo_small: str = Field(default="", alias="logoSmall")
    overview: str = Field(default="")
    picture: str = Field(default="")
    tooltip: str = Field(default="")
    version: str = Field(default="")


class ModificationBuild(BaseModel):
    binarize: bool = Field(default=False)
    rapify: bool = Field(default=False)
    include: list[str] = Field(default=MODIFICATION_BUILD_INCLUDE_FILES)


class ModificationLaunch(BaseModel):
    patching: bool = Field(default=False)


class ModificationConfiguration(BaseModel):
    enabled: bool = Field(default=True)
    serverside: bool = Field(default=False)
    build: ModificationBuild = Field(default_factory=ModificationBuild)
    launch: ModificationLaunch = Field(default_factory=ModificationLaunch)


class Modification(BaseModel):
    name: str
    prefix: str
    author: str
    configuration: ModificationConfiguration = Field(
        default_factory=ModificationConfiguration
    )

    details: ModificationDetails = Field(default_factory=ModificationDetails)
