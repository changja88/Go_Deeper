from applications.common.enum import Gender
from applications.common.type import MemberID
from application.meta_context.context_layer.subscriber.member_meta_request_event_sub import (
    MemberMetaRequestEventSubscriber,
)


class MemberMetaRequestEventPublisher:
    @classmethod
    def publish_member_gender_request_event(cls, member_id: MemberID) -> Gender:
        return MemberMetaRequestEventSubscriber.subscribe_member_gender_request_event(member_id=member_id)
