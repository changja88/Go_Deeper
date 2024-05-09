from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import (
    get_list_or_none,
    get_obj_or_none,
)
from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.django_meta.models import (
    EducationMetaPresetORM,
)


class EducationMetaLookupReadRepository:
    def find_all_by_meta_type(self, meta_type: UniversityType) -> list[Meta]:
        education_meta_preset_orm_list: Optional[list[EducationMetaPresetORM]] = get_list_or_none(
            EducationMetaPresetORM, type=meta_type, is_show=True
        )
        meta_list: list[Meta] = []
        if education_meta_preset_orm_list:
            for meta_orm in education_meta_preset_orm_list:
                meta_list.append(Meta(id=meta_orm.id, value=meta_orm.value, type=UniversityType(meta_orm.type)))
        return meta_list

    def find_by_id(self, meta_id: PositiveInt) -> Optional[Meta]:
        meta_preset_orm: Optional[EducationMetaPresetORM] = get_obj_or_none(EducationMetaPresetORM, id=meta_id)
        if meta_preset_orm:
            return Meta(id=meta_preset_orm.id, value=meta_preset_orm.value, type=UniversityType(meta_preset_orm.type))
        return None

    def search_meta_list_by(self, meta_type: UniversityType, search_text: str) -> list[Meta]:
        education_meta_preset_orm_list: Optional[list[EducationMetaPresetORM]] = get_list_or_none(
            EducationMetaPresetORM, value__contains=search_text, type=meta_type, is_show=True
        )
        meta_list: list[Meta] = []
        if education_meta_preset_orm_list:
            for meta_orm in education_meta_preset_orm_list:
                meta_list.append(Meta(id=meta_orm.id, value=meta_orm.value, type=UniversityType(meta_orm.type)))
        return meta_list

    def find_value_by(self, meta_id: PositiveInt) -> Optional[str]:
        education_meta_orm: Optional[EducationMetaPresetORM] = get_obj_or_none(EducationMetaPresetORM, id=meta_id)
        if education_meta_orm and education_meta_orm.value:
            value: str = education_meta_orm.value
            return value
        return None

    def find_type_by(self, meta_id: PositiveInt) -> Optional[UniversityType]:
        education_meta_orm: Optional[EducationMetaPresetORM] = get_obj_or_none(EducationMetaPresetORM, id=meta_id)
        if education_meta_orm and education_meta_orm.type:
            education_meta_type: UniversityType = UniversityType(education_meta_orm.type)
            return education_meta_type
        return None


class EducationMetaLookupWriteRepository:
    def get_or_create_custom_meta(self, custom_value: str, education_meta_type: UniversityType) -> Meta:
        meta_preset_orm, _ = EducationMetaPresetORM.objects.get_or_create(
            value=custom_value,
            type=education_meta_type,
            defaults={"value": custom_value, "type": education_meta_type, "is_show": False},
        )
        return Meta(
            id=meta_preset_orm.id,
            value=meta_preset_orm.value,
            type=UniversityType(meta_preset_orm.type),
        )


class EducationMetaLookupCompoundRepository(EducationMetaLookupReadRepository, EducationMetaLookupWriteRepository): ...
