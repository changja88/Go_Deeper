from typing import Optional

from django.core.files.uploadedfile import UploadedFile
from ninja import File
from pydantic import Field, PositiveInt, StrictBool

from applications.common.ninja.custom_entity_model import ValueObject
from application.meta_context.domain_layer.meta_enum import CensorStatus, PhotoType


class Photo(ValueObject):
    id: Optional[PositiveInt] = None
    file: File[UploadedFile] | str
    censor_status: CensorStatus = Field(default=CensorStatus.UNDER_CENSOR)
    is_main: StrictBool = False
    is_deleted: StrictBool = False
    rejected_reason: Optional[str] = None
    type: PhotoType

    def set_is_delete_as(self, is_deleted: bool) -> None:
        self.is_deleted = is_deleted

    def set_is_main_as(self, is_main: bool) -> None:
        self.is_main = is_main
