from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import get_list_or_none
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import PhysicalMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.django_meta.models import (
    MemberPhysicalMetaORM,
    PhysicalMetaPresetORM,
)


class MemberPhysicalMeteReadRepository:
    member_id: MemberID

    def __init__(self, member_id: MemberID) -> None:
        self.member_id = member_id

    def all_meta(self) -> list[Meta]:
        member_meta_list: list[Meta] = list()
        member_meta_orm_list: Optional[list[MemberPhysicalMetaORM]]
        if member_meta_orm_list := get_list_or_none(MemberPhysicalMetaORM, member_id=self.member_id):
            for member_meta_orm in member_meta_orm_list:
                member_meta_list.append(
                    Meta(
                        id=member_meta_orm.physical_meta.id,
                        value=member_meta_orm.physical_meta.value,
                        type=PhysicalMetaType(member_meta_orm.physical_meta.type),
                    )
                )
        return member_meta_list

    def find_by_type(self, physical_meta_type: PhysicalMetaType) -> Optional[Meta]:
        for meta in self.all_meta():
            if meta.type == physical_meta_type:
                return meta
        return None


class MemberPhysicalMetaWriteRepository:
    def create_or_update_weight_meta(self, member_id: MemberID, weight_meta_id: PositiveInt) -> Meta:
        member_physical_meta_orm, _ = MemberPhysicalMetaORM.objects.update_or_create(
            member_id=member_id,
            physical_meta__type=PhysicalMetaType.WEIGHT,
            defaults={"physical_meta_id": weight_meta_id},
        )
        return self._parse_to_meta_preset_unit(member_physical_meta_orm.physical_meta)

    def create_or_update_height_meta(self, member_id: MemberID, height_meta_id: PositiveInt) -> Meta:
        member_physical_meta_orm, _ = MemberPhysicalMetaORM.objects.update_or_create(
            member_id=member_id,
            physical_meta__type=PhysicalMetaType.HEIGHT,
            defaults={"physical_meta_id": height_meta_id},
        )
        return self._parse_to_meta_preset_unit(member_physical_meta_orm.physical_meta)

    def create_or_update_body_shape_meta(self, member_id: MemberID, body_shape_meta_id: PositiveInt) -> Meta:
        member_physical_meta_orm, _ = MemberPhysicalMetaORM.objects.update_or_create(
            member_id=member_id,
            physical_meta__type=PhysicalMetaType.BODY_SHAPE,
            defaults={"physical_meta_id": body_shape_meta_id},
        )
        return self._parse_to_meta_preset_unit(member_physical_meta_orm.physical_meta)

    def _parse_to_meta_preset_unit(self, physical_meta_orm: PhysicalMetaPresetORM) -> Meta:
        return Meta(
            id=physical_meta_orm.id, type=PhysicalMetaType(physical_meta_orm.type), value=physical_meta_orm.value
        )


class MemberPhysicalMetaCompoundRepository(MemberPhysicalMeteReadRepository, MemberPhysicalMetaWriteRepository):
    pass
