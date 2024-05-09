from typing import Optional

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.type import MemberID
from application.wanted_context.domain_layer.value_object.wanted_weight import (
    WantedWeight,
)
from application.wanted_context.infra_layer.django_wanted.models import (
    MemberWantedWeightORM,
)


class MemberWantedWeightReadRepository:
    def find_by_member_id(self, member_id: MemberID) -> WantedWeight:
        member_wanted_weight_orm: Optional[MemberWantedWeightORM]
        if member_wanted_weight_orm := get_obj_or_none(MemberWantedWeightORM, member_id=member_id):
            member_wanted_weight: WantedWeight = WantedWeight.model_validate(member_wanted_weight_orm)
            return member_wanted_weight
        return WantedWeight()


class MemberWantedWeightWriteRepository:

    def update_or_create(self, member_id: MemberID, member_wanted_weight: WantedWeight) -> WantedWeight:
        member_wanted_weight_orm: MemberWantedWeightORM
        member_wanted_weight_orm, _ = MemberWantedWeightORM.objects.update_or_create(
            member_id=member_id,
            defaults={
                "appearance_weight": member_wanted_weight.appearance_weight,
                "birth_year_weight": member_wanted_weight.birth_year_weight,
                "work_weight": member_wanted_weight.work_weight,
                "income_weight": member_wanted_weight.income_weight,
                "asset_weight": member_wanted_weight.asset_weight,
                "education_weight": member_wanted_weight.education_weight,
                "background_weight": member_wanted_weight.background_weight,
            },
        )
        saved_member_wanted_weight: WantedWeight = WantedWeight.model_validate(member_wanted_weight_orm)
        return saved_member_wanted_weight


class MemberWantedCompoundReadRepository(MemberWantedWeightWriteRepository, MemberWantedWeightReadRepository):
    pass
