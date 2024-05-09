from datetime import datetime
from typing import Annotated, Optional

from annotated_types import Gt, Lt, MaxLen
from ninja import Schema

from applications.common.enum import Gender
from applications.common.ninja.custom_entity_model import ValueObject
from application.meta_context.domain_layer.meta_enum import PhotoType


class IntroductionChangeSchemaIn(Schema):
    introduction: str


class MemberPhotoRegisterSchemaIn(Schema):
    photo_type: PhotoType
    is_main: bool


class MemberPhotoUpdateSchemaIn(Schema):
    photo_id: int
    is_main: Optional[bool]
    is_deleted: Optional[bool]


class RegistrationSchemaIn(ValueObject):
    name: Annotated[str, MaxLen(20)]
    phone_number: Annotated[str, MaxLen(20)]
    nickname: Annotated[str, MaxLen(8)]
    gender: Gender
    birth_year: Annotated[int, Gt(1900), Lt(datetime.now().year)]
