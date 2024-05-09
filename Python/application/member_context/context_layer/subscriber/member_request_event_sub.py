from typing import Optional

from applications.common.type import MemberID
from applications.member.domain_layer.entity.member import Member
from application.member_context.infra_layer.service.member_service import MemberService


class MemberRequestEventSubscriber:
    @classmethod
    def subscribe_member_request_event(cls, member_id: MemberID) -> Optional[Member]:
        return MemberService().find_by_member_id(member_id=member_id)
