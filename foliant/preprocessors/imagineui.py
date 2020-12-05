'''
Preprocessor for Foliant documentation authoring tool.
Renders ImagineUI wireframes and inserts them into documents.

Uses Node.js, headless Chrome, Puppeteer and ImagineUI.
'''

import re
from pathlib import Path
from hashlib import md5
from subprocess import run, PIPE, STDOUT, CalledProcessError
from time import sleep
from typing import Dict

OptionValue = int or float or bool or str

from foliant.utils import output
from foliant.preprocessors.base import BasePreprocessor


class Preprocessor(BasePreprocessor):
    defaults = {
        'version': 'latest',
        'cache_dir': Path('.imagineuicache'),
    }

    tags = 'imagineui',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._cache_dir_path = (self.project_path / self.options['cache_dir']).resolve()

        self.logger = self.logger.getChild('imagineui')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

    def _scene_filepath(self, name):
        return f'{self._cache_dir_path}/{name}.scene'

    def _rendered_scene_filepath(self, name):
        return f'{self._cache_dir_path}/{name}.png'

    def _process_imagineui(self, name: str) -> str:
        # TODO: Get caption from IUI syntax
        return f'![ImagineUI Render]({self._rendered_scene_filepath(name)})'

    i = -1

    def _get_substitution_count(self):
        self.i += 1
        return self.i

    def process_imagineui(self, markdown_content: str) -> str:
        def _sub(wireframe_definition) -> str:
            return self._process_imagineui(f"{self._get_substitution_count()}")

        return self.pattern.sub(_sub, markdown_content)

    def apply(self):
        self.logger.info('Applying preprocessor')

        wireframe_files = []

        # fixme: hash .scene file names
        i = 0
        for markdown_file_path in self.working_dir.rglob('*.md'):
            with open(markdown_file_path, encoding='utf8') as markdown_file:
                markdown_content = markdown_file.read()

            wireframe_definitions = re.finditer(self.pattern, markdown_content)

            for wireframe_definition in wireframe_definitions:
                wireframe_file_path = self._scene_filepath(i)
                i += 1
                with open(wireframe_file_path, 'w', encoding='utf8') as wireframe_file:
                    wireframe_file.write(wireframe_definition.group('body').strip())
                wireframe_files.append(wireframe_file_path)

        self.logger.debug(f'Wireframe files: {wireframe_files}')

        if wireframe_files:
            self._cache_dir_path.mkdir(parents=True, exist_ok=True)

            output('Running ImagineUI CLI', self.quiet)

            input_param = " ".join(map(lambda x: f'--input=' + x, wireframe_files))

            ver = self.options["version"]
            package_name = "imagineui-cli"
            if ver and ver != "latest":
                package_name = f'imagineui-cli@{self.options["version"]}'

            command = (
                    f'npx {package_name} ' +
                    f'--outputDir={self._cache_dir_path} ' +
                    input_param
            )

            command_output = run(command, shell=True, check=True, stdout=PIPE, stderr=STDOUT)

            if command_output.stdout:
                output(command_output.stdout.decode('utf8', errors='ignore'), self.quiet)

            for markdown_file_path in self.working_dir.rglob('*.md'):
                with open(markdown_file_path, encoding='utf8') as markdown_file:
                    markdown_content = markdown_file.read()

                processed_content = self.process_imagineui(markdown_content)

                if processed_content:
                    with open(markdown_file_path, 'w', encoding='utf8') as markdown_file:
                        markdown_file.write(processed_content)

        self.logger.info('Preprocessor applied')
