
from typing import Optional

from distlib.util import cached_property
from pydantic import PositiveInt

from applications.common.django.django_model_util import get_list_or_none
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import (
    MULTI_SELECTION_PREFERENCE_META,
    SINGLE_SELECTION_PREFERENCE_META,
    PreferenceMetaType,
)
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.django_meta.models import (
    MemberPreferenceMetaORM,
)


class MemberPreferenceMetaReadRepository:

    member_id: MemberID

    def __init__(self, member_id: MemberID) -> None:
        self.member_id = member_id

    @cached_property
    def all_meta(self) -> list[Meta]:
        member_preference_meta_list: list[Meta] = []
        if member_preference_orm_list := get_list_or_none(MemberPreferenceMetaORM, member_id=self.member_id):
            for member_preference_meta_orm in member_preference_orm_list:
                member_preference_meta_list.append(
                    Meta(
                        id=member_preference_meta_orm.preference_meta.id,
                        value=member_preference_meta_orm.preference_meta.value,
                        type=PreferenceMetaType(member_preference_meta_orm.preference_meta.type),
                    )
                )
        return member_preference_meta_list

    def find_by_type(self, meta_type: PreferenceMetaType) -> Optional[list[Meta]] | Optional[Meta]:
        if meta_type in SINGLE_SELECTION_PREFERENCE_META:
            meta: Meta
            for meta in self.all_meta:
                if meta.type == meta_type:
                    return meta
        elif meta_type in MULTI_SELECTION_PREFERENCE_META:
            meta_list: list[Meta] = list()
            for meta in self.all_meta:
                if meta.type == meta_type:
                    meta_list.append(meta)
            return meta_list
        return None


class MemberPreferenceMetaWriteRepository:
    def update_or_create(self, meta_id: PositiveInt, member_id: PositiveInt, meta_type: PreferenceMetaType) -> Meta:
        member_preference_orm: MemberPreferenceMetaORM
        member_preference_orm, _ = MemberPreferenceMetaORM.objects.update_or_create(
            member_id=member_id,
            preference_meta__type=meta_type,
            defaults={"preference_meta_id": meta_id, "member_id": member_id},
        )
        return Meta(
            id=member_preference_orm.preference_meta.id,
            type=PreferenceMetaType(member_preference_orm.preference_meta.type),
            value=member_preference_orm.preference_meta.value,
        )

    def create(self, meta_id: PositiveInt, member_id: PositiveInt) -> Meta:
        member_preference_meta_orm: MemberPreferenceMetaORM = MemberPreferenceMetaORM.objects.create(
            member_id=member_id, preference_meta_id=meta_id
        )
        return Meta(
            id=member_preference_meta_orm.preference_meta.id,
            type=PreferenceMetaType(member_preference_meta_orm.preference_meta.type),
            value=member_preference_meta_orm.preference_meta.value,
        )

    def delete_same_type_meta_by(self, meta_type: PreferenceMetaType, member_id: PositiveInt) -> None:
        MemberPreferenceMetaORM.objects.filter(member_id=member_id, preference_meta__type=meta_type).delete()


class MemberPreferenceMetaCompoundRepository(
    MemberPreferenceMetaReadRepository, MemberPreferenceMetaWriteRepository
): ...
