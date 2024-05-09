from django.core.files.uploadedfile import UploadedFile
from ninja import File
from pydantic import Field, PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject


class CertificationFile(ValueObject):
    id: PositiveInt
    file: File[UploadedFile] | str
    is_deleted: bool = Field(default=False)
