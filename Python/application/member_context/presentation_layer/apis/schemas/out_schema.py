from ninja import Schema
from pydantic import Field, StrictBool

from applications.member.domain_layer.entity.member import Member
from applications.member.domain_layer.entity.member_address import MemberAddress
from applications.member.domain_layer.value_object.address import (
    Address,
    AddressUnit,
)
from applications.member.domain_layer.value_object.enum import MemberStatus
from applications.member.domain_layer.value_object.unique_info import UniqueInfo
from application.member_context.infra_layer.django.models import BearerTokenORM
from application.meta_context.domain_layer.value_object.meta.photo import Photo


class BearerTokenOutSchema(Schema):
    key: str = Field(None, serialization_alias="token")

    class Config(Schema.Config):
        model = BearerTokenORM
        model_fields = ["key"]
        populate_by_name = True


class MemberOutSchema(Schema):
    id: int
    unique_info: UniqueInfo
    status: MemberStatus
    friend_code: str
    introduction: str

    class Config:
        model = Member
        model_fields = ["id", "unique_info", "status", "friend_code", "introduction"]


class MemberPhotoOutSchema(Schema):
    member_id: int
    photos: list[Photo]


class MemberAddressOutSchema(Schema):
    member_id: int
    playing_address: Address
    living_address: Address

    class Config(Schema.Config):
        model = MemberAddress
        model_fields = ["member_id", "playing_address", "living_address"]


class MemberDuplicationOutSchema(Schema):
    is_able: StrictBool


class AddressLookupOutSchema(Schema):
    address_list: list[AddressUnit]
