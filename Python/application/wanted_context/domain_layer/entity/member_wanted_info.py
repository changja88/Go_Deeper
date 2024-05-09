from typing import List, Self

from pydantic import Field, NonNegativeInt, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.wanted_context.domain_layer.value_object.wanted_preference import (
    WantedPreference,
)
from application.wanted_context.domain_layer.value_object.wanted_weight import (
    WantedWeight,
)
from application.wanted_context.infra_layer.repository.member_wanted_preference_repositories import (
    MemberWantedPreferenceCompoundRepository,
)
from application.wanted_context.infra_layer.repository.member_wanted_repositories import (
    MemberWantedCompoundReadRepository,
)


class MemberWantedInfo(ValueObject):
    member_id: MemberID
    wanted_weight: WantedWeight
    wanted_preference: WantedPreference
    weight_repo: SkipJsonSchema[MemberWantedCompoundReadRepository] = Field(exclude=True)
    preference_repo: SkipJsonSchema[MemberWantedPreferenceCompoundRepository] = Field(exclude=True)

    def __init__(
        self,
        member_id: MemberID,
        weight_repo: MemberWantedCompoundReadRepository = MemberWantedCompoundReadRepository(),
        preference_repo: MemberWantedPreferenceCompoundRepository = MemberWantedPreferenceCompoundRepository(),
    ):
        super().__init__(
            member_id=member_id,
            wanted_weight=weight_repo.find_by_member_id(member_id=member_id),
            weight_repo=weight_repo,
            wanted_preference=WantedPreference(
                alcohol_preference_meta_ids=preference_repo.find_all_preference_type(
                    member_id=member_id, preference_type=PreferenceMetaType.ALCOHOL
                ),
                smoke_preference_meta_ids=preference_repo.find_all_preference_type(
                    member_id=member_id, preference_type=PreferenceMetaType.SMOKING
                ),
                religion_preference_meta_ids=preference_repo.find_all_preference_type(
                    member_id=member_id, preference_type=PreferenceMetaType.RELIGION
                ),
                hobby_preference_meta_ids=preference_repo.find_all_preference_type(
                    member_id=member_id, preference_type=PreferenceMetaType.HOBBY
                ),
            ),
            preference_repo=preference_repo,
        )

    def register_wanted_weight_appearance_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_appearance_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_weight_birth_year_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_birth_year_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_weight_work_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_job_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_weight_income_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_income_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_weight_asset_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_asset_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_weight_education_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_education_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_weight_background_weight(self, weight: NonNegativeInt) -> Self:
        self.wanted_weight.set_background_weight(weight)
        self.weight_repo.update_or_create(member_id=self.member_id, member_wanted_weight=self.wanted_weight)
        return self

    def register_wanted_preference_metas(self, meta_ids: List[int], preference_type: PreferenceMetaType) -> Self:
        preference_meta_ids: list[PositiveInt] = self.preference_repo.delete_and_recreate(
            member_id=self.member_id, preference_type=preference_type, preference_meta_ids=meta_ids
        )
        if preference_type == PreferenceMetaType.RELIGION:
            self.wanted_preference.set_religion_preference_meta_ids(meta_ids=preference_meta_ids)
        elif preference_type == PreferenceMetaType.HOBBY:
            self.wanted_preference.set_hobby_preference_meta_ids(meta_ids=preference_meta_ids)
        elif preference_type == PreferenceMetaType.ALCOHOL:
            self.wanted_preference.set_alcohol_preference_meta_ids(meta_ids=preference_meta_ids)
        elif preference_type == PreferenceMetaType.SMOKING:
            self.wanted_preference.set_smoke_preference_meta_ids(meta_ids=preference_meta_ids)
        return self
