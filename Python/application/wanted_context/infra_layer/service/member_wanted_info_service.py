from typing import Optional

from pydantic import Field, PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.wanted_context.domain_layer.entity.member_wanted_info import (
    MemberWantedInfo,
)


class WantedWeightRegisterRequest(ValueObject):
    member_id: MemberID
    appearance_weight: Optional[PositiveInt] = Field(default=None)
    birth_year_weight: Optional[PositiveInt] = Field(default=None)
    work_weight: Optional[PositiveInt] = Field(default=None)
    income_weight: Optional[PositiveInt] = Field(default=None)
    asset_weight: Optional[PositiveInt] = Field(default=None)
    education_weight: Optional[PositiveInt] = Field(default=None)
    background_weight: Optional[PositiveInt] = Field(default=None)


class WantedPreferenceRegisterRequest(ValueObject):
    member_id: MemberID
    preference_type: PreferenceMetaType
    meta_ids: list[PositiveInt]


class MemberWantedInfoService:

    def find_by_member_id(self, member_id: MemberID) -> MemberWantedInfo:
        return MemberWantedInfo(member_id=member_id)

    def register_member_wanted_weight(
        self, wanted_weight_register_request: WantedWeightRegisterRequest
    ) -> MemberWantedInfo:
        member_wanted_info: MemberWantedInfo = MemberWantedInfo(member_id=wanted_weight_register_request.member_id)
        if weight := wanted_weight_register_request.appearance_weight:
            member_wanted_info.register_wanted_weight_appearance_weight(weight=weight)
        if weight := wanted_weight_register_request.birth_year_weight:
            member_wanted_info.register_wanted_weight_birth_year_weight(weight=weight)
        if weight := wanted_weight_register_request.work_weight:
            member_wanted_info.register_wanted_weight_work_weight(weight=weight)
        if weight := wanted_weight_register_request.income_weight:
            member_wanted_info.register_wanted_weight_income_weight(weight=weight)
        if weight := wanted_weight_register_request.asset_weight:
            member_wanted_info.register_wanted_weight_asset_weight(weight=weight)
        if weight := wanted_weight_register_request.education_weight:
            member_wanted_info.register_wanted_weight_education_weight(weight=weight)
        if weight := wanted_weight_register_request.background_weight:
            member_wanted_info.register_wanted_weight_background_weight(weight=weight)

        return member_wanted_info

    def register_member_wanted_preference(
        self, wanted_preference_register_request: WantedPreferenceRegisterRequest
    ) -> MemberWantedInfo:
        member_wanted_info: MemberWantedInfo = MemberWantedInfo(member_id=wanted_preference_register_request.member_id)
        member_wanted_info.register_wanted_preference_metas(
            meta_ids=wanted_preference_register_request.meta_ids,
            preference_type=wanted_preference_register_request.preference_type,
        )
        return member_wanted_info
