from dzmt.constants import MODIFICATION_FILE
from dzmt.models.modification import Modification
from dzmt.utils.helpers import preformat
from dzmt.utils.serializers import Serializer

from .base import Template
from .constants import CONFIG_CPP_CONTENT


class ModificationTemplate(Template):
    config_content = CONFIG_CPP_CONTENT

    def __init__(self, config: Modification, serializer: Serializer):
        self._config = config
        self._serializer = serializer

    def get_template(self):
        return {
            "Scripts": {
                "kind": "directory",
                "spec": {
                    "3_Game": {
                        "kind": "directory",
                        "spec": {".gitkeep": {"kind": "file", "spec": {"content": ""}}},
                    },
                    "4_World": {
                        "kind": "directory",
                        "spec": {".gitkeep": {"kind": "file", "spec": {"content": ""}}},
                    },
                    "5_Mission": {
                        "kind": "directory",
                        "spec": {".gitkeep": {"kind": "file", "spec": {"content": ""}}},
                    },
                },
            },
            "config.cpp": {
                "kind": "file",
                "spec": {
                    "content": preformat(self.config_content).format(
                        name=self._config.name,
                        prefix=self._config.prefix,
                        author=self._config.author,
                    )
                },
            },
            f"{MODIFICATION_FILE}.{self._get_extension()}": {
                "kind": "file",
                "spec": {
                    "content": self._serializer.dump(
                        self._config.model_dump(by_alias=True)
                    )
                },
            },
        }

    def _get_extension(self):
        return self._serializer.extension
