from applications.common.django.django_model_util import get_list_or_none
from applications.member.domain_layer.value_object.address import AddressUnit
from application.member_context.infra_layer.django.models import (
    AddressLevel1ORM,
    AddressLevel2ORM,
)


class AddressReadRepository:
    def find_lv1_address(self) -> list[AddressUnit] | None:
        address_list: list[AddressUnit] = list()
        if lv1_address_orm_list := get_list_or_none(AddressLevel1ORM):
            for address in lv1_address_orm_list:
                address_list.append(AddressUnit.model_validate(address))
            return address_list
        return None

    def find_lv2_address(self, lv1_id: int) -> list[AddressUnit] | None:
        if lv2_address_orm_list := get_list_or_none(AddressLevel2ORM, level1_id=lv1_id):
            address_list: list[AddressUnit] = list()
            for address in lv2_address_orm_list:
                address_list.append(AddressUnit.model_validate(address))
            return address_list
        return None


class AddressWriteRepository: ...


class AddressCompoundRepository(AddressReadRepository, AddressWriteRepository): ...
