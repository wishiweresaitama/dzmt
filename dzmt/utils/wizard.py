from pathlib import Path

from dzmt.core.generator.generator import ContentGenerator
from dzmt.core.template.base import Template


class Wizard:
    def __init__(
        self,
        root: Path,
        template: Template,
    ):
        self.root = root
        self.template = template

    def run(self):
        self._generate()

    def _generate(self):
        ContentGenerator(self.template, self.root).generate()
