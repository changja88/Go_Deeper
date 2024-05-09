from typing import Optional

from applications.common.type import MemberID
from application.member_context.context_layer.subscriber.member_request_event_sub import (
    MemberRequestEventSubscriber,
)
from applications.member.domain_layer.entity.member import Member


class MemberRequestEventPublisher:
    @classmethod
    def publish_member_request_event(cls, member_id: MemberID) -> Optional[Member]:
        return MemberRequestEventSubscriber.subscribe_member_request_event(member_id=member_id)
