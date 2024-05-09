from typing import Optional

from applications.common.type import MemberID
from applications.member.domain_layer.entity.member_address import MemberAddress
from applications.member.domain_layer.value_object.address import AddressIdSet


class MemberAddressService:
    def find_by_id(self, member_id: MemberID) -> Optional[MemberAddress]:
        return MemberAddress(member_id=member_id)

    def register_member_playing_address(self, member_id: MemberID, address_id_set: AddressIdSet) -> MemberAddress:
        return MemberAddress(member_id=member_id).register_playing_address(address_id_set)

    def register_member_living_address(self, member_id: MemberID, address_id_set: AddressIdSet) -> MemberAddress:
        return MemberAddress(member_id=member_id).register_living_address(address_id_set)
