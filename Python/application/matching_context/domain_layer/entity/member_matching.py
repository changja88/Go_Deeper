from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.matching_context.domain_layer.matching_enum import MatchingStatus


class MemberMatching(ValueObject):
    to_member_id: MemberID
    from_member_id: MemberID
    status: MatchingStatus
