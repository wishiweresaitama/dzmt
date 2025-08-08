from dzmt.constants import PROJECT_DIR, PROJECT_FILE
from dzmt.models.project import Project
from dzmt.utils.serializers import Serializer

from .base import Template


class ProjectTemplate(Template):
    def __init__(self, config: Project, serializer: Serializer):
        self._config = config
        self._serializer = serializer

    def get_template(self):
        return {
            PROJECT_DIR: {
                "kind": "directory",
                "spec": {
                    f"{PROJECT_FILE}.{self._get_extension()}": {
                        "kind": "file",
                        "spec": {
                            "content": self._serializer.dump(self._config.model_dump())
                        },
                    }
                },
            }
        }

    def _get_extension(self):
        return self._serializer.extension
