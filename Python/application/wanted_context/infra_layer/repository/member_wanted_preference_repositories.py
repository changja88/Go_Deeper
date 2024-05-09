from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.meta_context.infra_layer.django_meta.models import (
    PreferenceMetaPresetORM,
)
from application.wanted_context.infra_layer.django_wanted.models import (
    MemberWantedPreferenceORM,
    MemberWantedPreferenceToPreferenceMetaPresetORM,
)


class MemberWantedPreferenceReadRepository:
    def find_all_preference_type(self, member_id: MemberID, preference_type: PreferenceMetaType) -> list[PositiveInt]:
        member_wanted_preference_ids: list[PositiveInt] = list()

        member_wanted_preference_meta_orm: Optional[MemberWantedPreferenceORM]
        if member_wanted_preference_meta_orm := get_obj_or_none(MemberWantedPreferenceORM, member_id=member_id):
            preference_meta_preset: PreferenceMetaPresetORM
            for preference_meta_preset in member_wanted_preference_meta_orm.preference_metas.all():
                if preference_meta_preset.type == preference_type:
                    member_wanted_preference_ids.append(preference_meta_preset.id)

        return member_wanted_preference_ids


class MemberWantedPreferenceWriteRepository:
    def delete_and_recreate(
        self, member_id: MemberID, preference_meta_ids: list[PositiveInt], preference_type: PreferenceMetaType
    ) -> list[PositiveInt]:
        member_wanted_preference_orm, _ = MemberWantedPreferenceORM.objects.get_or_create(member_id=member_id)

        MemberWantedPreferenceToPreferenceMetaPresetORM.objects.filter(
            member_wanted_preference_id=member_wanted_preference_orm.id,
            preference_meta_preset__type=preference_type,
        ).delete()

        member_wanted_preference_id_list: list[PositiveInt] = list()
        for preference_id in preference_meta_ids:
            obj = MemberWantedPreferenceToPreferenceMetaPresetORM.objects.create(
                preference_meta_preset_id=preference_id,
                member_wanted_preference_id=member_wanted_preference_orm.id,
            )
            member_wanted_preference_id_list.append(obj.preference_meta_preset_id)
        return member_wanted_preference_id_list


class MemberWantedPreferenceCompoundRepository(
    MemberWantedPreferenceReadRepository, MemberWantedPreferenceWriteRepository
):
    pass
