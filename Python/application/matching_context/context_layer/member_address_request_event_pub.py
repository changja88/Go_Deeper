from typing import Optional

from applications.common.type import MemberID
from application.member_context.context_layer.subscriber.member_address_reqeust_event_sub import (
    MemberAddressRequestEventSubscriber,
)
from applications.member.domain_layer.entity.member_address import MemberAddress


class MemberAddressRequestEventPublisher:
    @classmethod
    def publish_address_request_event(cls, member_id: MemberID) -> Optional[MemberAddress]:
        return MemberAddressRequestEventSubscriber.subscribe_address_request_event(member_id=member_id)
