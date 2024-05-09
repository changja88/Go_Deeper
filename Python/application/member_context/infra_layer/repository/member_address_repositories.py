from typing import Optional

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.type import MemberID
from applications.member.domain_layer.value_object.address import (
    Address,
    AddressIdSet,
    AddressUnit,
    AddressWithCertification,
)
from application.member_context.infra_layer.django.models.address_orm import (
    MemberLivingAddressORM,
    MemberPlayingAddressORM,
)
from application.meta_context.domain_layer.meta_enum import CensorStatus


class MemberAddressReadRepository:
    def find_playing_address(self, member_id: MemberID) -> Optional[Address]:
        if playing_address_orm := get_obj_or_none(MemberPlayingAddressORM, member_id=member_id):
            address: Address = Address.model_validate(playing_address_orm)
            return address
        return None

    def find_living_address(self, member_id: MemberID) -> Optional[Address]:
        if playing_address_orm := get_obj_or_none(MemberLivingAddressORM, member_id=member_id):
            address: Address = Address.model_validate(playing_address_orm)
            return address
        return None


class MemberAddressWriteRepository:
    def create_or_update_playing_address(self, member_id: MemberID, playing_address_id_set: AddressIdSet) -> Address:
        playing_address_orm, _ = MemberPlayingAddressORM.objects.update_or_create(
            member_id=member_id, defaults=playing_address_id_set.model_dump()
        )
        playing_address: Address = Address.model_validate(playing_address_orm)
        return playing_address

    def create_or_update_living_address(
        self, member_id: MemberID, living_address_id_set: AddressIdSet
    ) -> AddressWithCertification:
        living_address_orm, _ = MemberLivingAddressORM.objects.update_or_create(
            member_id=member_id, defaults=living_address_id_set.model_dump()
        )
        living_address: AddressWithCertification = AddressWithCertification(
            level1=AddressUnit(id=living_address_orm.level1.id, name=living_address_orm.level1.name),
            level2=AddressUnit(id=living_address_orm.level2.id, name=living_address_orm.level2.name),
            is_certified=True if living_address_orm.censor_status == CensorStatus.APPROVED else False,
        )
        return living_address


class MemberAddressCompoundRepository(MemberAddressWriteRepository, MemberAddressReadRepository): ...
