from ninja import Schema
from pydantic import PositiveInt

from application.meta_context.domain_layer.meta_enum import PreferenceMetaType


class MemberPreferenceMetaSchemaIn(Schema):
    meta_id_list: list[PositiveInt]
    meta_type: PreferenceMetaType


class MemberFCMInfoSchemaIn(Schema):
    fcm_token: str
    device_info: str


class MemberMetaSchemaIn(Schema):
    meta_id: PositiveInt


class MemberMultipleMetaSchemaIn(Schema):
    meta_id_list: list[PositiveInt]


class MemberCustomMetaSchemaIn(Schema):
    meta_type: str
    custom_value: str


class MetaCertificationSchemaIn(Schema):
    certification_id: str
