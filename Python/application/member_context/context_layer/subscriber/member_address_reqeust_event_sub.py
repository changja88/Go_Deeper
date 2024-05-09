from typing import Optional

from applications.common.type import MemberID
from applications.member.domain_layer.entity.member_address import MemberAddress
from application.member_context.infra_layer.service.member_address_service import (
    MemberAddressService,
)


class MemberAddressRequestEventSubscriber:
    @classmethod
    def subscribe_address_request_event(cls, member_id: MemberID) -> Optional[MemberAddress]:
        return MemberAddressService().find_by_id(member_id=member_id)
