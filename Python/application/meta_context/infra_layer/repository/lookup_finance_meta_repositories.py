from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import (
    get_list_or_none,
    get_obj_or_none,
)
from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.django_meta.models import FinanceMetaPresetORM


class FinanceMetaLookupReadRepository:

    def find_all_by_type(self, meta_type: FinanceMetaType) -> list[Meta]:
        meta_orm_list: Optional[list[FinanceMetaPresetORM]]
        meta_list: list[Meta] = []
        if meta_orm_list := get_list_or_none(FinanceMetaPresetORM, type=meta_type, is_show=True):
            for meta_orm in meta_orm_list:
                meta_list.append(self._parse_to_finance_meta(meta_orm))
        return meta_list

    def _parse_to_finance_meta(self, meta_orm: FinanceMetaPresetORM) -> Meta:
        return Meta(
            id=meta_orm.id,
            type=FinanceMetaType(meta_orm.type),
            value=meta_orm.value,
        )

    def find_by_id(self, meta_id: PositiveInt) -> Optional[Meta]:
        previous_meta_orm: Optional[FinanceMetaPresetORM]
        if previous_meta_orm := get_obj_or_none(FinanceMetaPresetORM, id=meta_id, is_show=True):
            return self._parse_to_finance_meta(previous_meta_orm)
        return None

    def search_meta_list_by(self, meta_type: FinanceMetaType, search_text: str) -> list[Meta]:
        finance_meta_preset_orm_list: Optional[list[FinanceMetaPresetORM]] = get_list_or_none(
            FinanceMetaPresetORM, value__contains=search_text, type=meta_type, is_show=True
        )
        meta_list: list[Meta] = []
        if finance_meta_preset_orm_list:
            for meta_orm in finance_meta_preset_orm_list:
                meta_list.append(self._parse_to_finance_meta(meta_orm))
        return meta_list


class FinanceMetaLookupWriteRepository:
    def get_or_create_custom_meta(self, meta_type: FinanceMetaType, custom_value: str) -> Meta:
        finance_meta: FinanceMetaPresetORM
        finance_meta, _ = FinanceMetaPresetORM.objects.get_or_create(
            type=meta_type,
            value=custom_value,
            defaults={"type": meta_type, "value": custom_value},
        )
        return Meta(
            id=finance_meta.id,
            type=FinanceMetaType(finance_meta.type),
            value=finance_meta.value,
        )


class FinanceMetaLookupCompoundRepository(FinanceMetaLookupReadRepository, FinanceMetaLookupWriteRepository):
    pass
