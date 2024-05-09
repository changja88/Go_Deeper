from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import (
    get_list_or_none,
    get_obj_or_none,
)
from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.django_meta.models import (
    PreferenceMetaPresetORM,
)


class PreferenceMetaLookupReadRepository:
    def find_by_type(self, meta_type: PreferenceMetaType) -> Optional[list[Meta]]:
        if preference_meta_orm_list := get_list_or_none(PreferenceMetaPresetORM, type=meta_type):
            preference_meta_list = []
            for preference_meta_orm in preference_meta_orm_list:
                preference_meta_list.append(
                    Meta(
                        id=preference_meta_orm.id,
                        value=preference_meta_orm.value,
                        type=PreferenceMetaType(preference_meta_orm.type),
                    )
                )
            return preference_meta_list
        return None

    def find_type_by(self, meta_id: PositiveInt) -> Optional[PreferenceMetaType]:
        preference_meta_orm: Optional[PreferenceMetaPresetORM] = get_obj_or_none(PreferenceMetaPresetORM, id=meta_id)
        if preference_meta_orm:
            return PreferenceMetaType(preference_meta_orm.type)
        return None

    def find_by(self, meta_id: PositiveInt) -> Optional[Meta]:
        preference_meta_orm: Optional[PreferenceMetaPresetORM] = get_obj_or_none(PreferenceMetaPresetORM, id=meta_id)
        if preference_meta_orm:
            return Meta(
                id=preference_meta_orm.id,
                type=PreferenceMetaType(preference_meta_orm.type),
                value=preference_meta_orm.value,
            )
        return None


class PreferenceMetaLookupWriteRepository: ...


class PreferenceMetaCompoundRepository(PreferenceMetaLookupReadRepository, PreferenceMetaLookupWriteRepository): ...
