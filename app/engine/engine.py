import io
from typing import Dict, List

from jinja2 import Template as JinjaTemplate

from .get_placeholder import get_placeholder
import pdfkit
local_funcs: List[str] = []


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

    def render(self, data: Dict[str, object]) -> io.BytesIO:
        result = pdfkit.from_string(self.__apply_template(data), output_path=False)
        _file = io.BytesIO()
        _file.write(result)
        return _file
