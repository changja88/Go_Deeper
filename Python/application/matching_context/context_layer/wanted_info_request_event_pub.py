from applications.common.type import MemberID
from application.wanted_context.context_layer.wanted_info_request_event_sub import (
    WantedInfoRequestEventSubscriber,
)
from application.wanted_context.domain_layer.entity.member_wanted_info import (
    MemberWantedInfo,
)


class WantedInfoRequestEventPublisher:
    @classmethod
    def publish_member_wanted_info_request_event(cls, member_id: MemberID) -> MemberWantedInfo:
        return WantedInfoRequestEventSubscriber.subscribe_member_wanted_info_reqeust_event(member_id=member_id)
