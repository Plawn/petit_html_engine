import io
from typing import Dict, List, Optional

import pdfkit
from jinja2 import Template as JinjaTemplate

from .get_placeholder import get_placeholder

local_funcs: List[str] = []


class BytesIO(io.BytesIO):
    @staticmethod
    def of(content: bytes):
        f = io.BytesIO()
        f.write(content)
        return f


class Template:

    def __init__(self, _file: io.BytesIO):
        self.fields: List[str] = list()
        self.content = _file.getvalue().decode('utf-8')
        self.template = JinjaTemplate(self.content)
        self.__load_fields()

    def __load_fields(self):
        self.fields = fields = get_placeholder(self.content, local_funcs)
        return fields

    def __apply_template(self, data: Dict[str, str]) -> str:
        """
        Applies the data to the template and returns a `Template`
        """
        return self.template.render(data)

    def render(self, data: Dict[str, object], options: Optional[List[str]]) -> io.BytesIO:
        rendered = self.__apply_template(data)
        # if need pdf conversion
        # if options is not None and 'pdf' in options:
        if True:
            rendered = pdfkit.from_string(rendered, output_path=False)
        return BytesIO.of(rendered)
