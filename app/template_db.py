from minio.api import Minio
from .utils import download_minio_stream
import time
from .datastructure import S3Path
import io
from dataclasses import dataclass
from typing import Dict, List, Optional
from .engine import Template


@dataclass
class TemplateContainer:
    templater: Template
    pulled_at: float


class TemplateDB:
    def __init__(self):
        self.__templates: Dict[str, TemplateContainer] = {}
        # should use a better s3 interface
        self.__s3_client: Optional[Minio] = None

    def set_s3_client(self, client: Minio) -> None:
        self.__s3_client = client

    def render_template(self, exposed_as: str, data: dict) -> io.BytesIO:
        return self.__templates[exposed_as].templater.render(data)

    def delete_template(self, exposed_as:str) -> None:
        del self.__templates[exposed_as]

    def add_template(self, s3_path: S3Path, exposed_as: str) -> Template:
        doc = self.__s3_client.get_object(s3_path.bucket, s3_path.path)
        _file = io.BytesIO()
        download_minio_stream(doc, _file)
        template = Template(_file)
        self.__templates[exposed_as] = TemplateContainer(template, time.time())
        return template

    def get_fields(self, exposed_as: str) -> List[str]:
        return self.__templates[exposed_as].templater.fields

    def get_containers(self) -> Dict[str, TemplateContainer]:
        return self.__templates
