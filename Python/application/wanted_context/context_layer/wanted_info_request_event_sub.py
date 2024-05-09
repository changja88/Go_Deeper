from applications.common.type import MemberID
from application.wanted_context.domain_layer.entity.member_wanted_info import (
    MemberWantedInfo,
)
from application.wanted_context.infra_layer.service.member_wanted_info_service import (
    MemberWantedInfoService,
)


class WantedInfoRequestEventSubscriber:
    @classmethod
    def subscribe_member_wanted_info_reqeust_event(cls, member_id: MemberID) -> MemberWantedInfo:
        return MemberWantedInfoService().find_by_member_id(member_id=member_id)
