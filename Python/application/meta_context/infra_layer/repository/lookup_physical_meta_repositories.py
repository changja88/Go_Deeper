from typing import Optional

from applications.common.django.django_model_util import get_obj_or_none
from application.meta_context.domain_layer.meta_enum import PhysicalMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.django_meta.models import (
    PhysicalMetaPresetORM,
)


class PhysicalMetaLookupReadRepository:
    def find_by_type(self, meta_type: PhysicalMetaType) -> list[Meta]:
        metas: list[Meta] = list()
        for physical_meta_preset_orm in PhysicalMetaPresetORM.objects.filter(type=meta_type):
            metas.append(
                Meta(
                    id=physical_meta_preset_orm.id,
                    value=physical_meta_preset_orm.value,
                    type=PhysicalMetaType(physical_meta_preset_orm.type),
                )
            )
        return metas

    def find_by_id(self, meta_id: int) -> Optional[Meta]:
        physical_meta_orm: Optional[PhysicalMetaPresetORM]
        if physical_meta_orm := get_obj_or_none(PhysicalMetaPresetORM, id=meta_id):
            return Meta(
                id=physical_meta_orm.id, type=PhysicalMetaType(physical_meta_orm.type), value=physical_meta_orm.value
            )
        return None


class PhysicalMetaLookupWriteRepository: ...


class PhysicalMetaLookupCompoundRepository(PhysicalMetaLookupWriteRepository, PhysicalMetaLookupReadRepository): ...
