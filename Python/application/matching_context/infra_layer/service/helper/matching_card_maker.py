from applications.common.type import MemberID
from application.matching_context.domain_layer.value_object.matching_card import (
    MatchingCard,
)


class MatchingCardMaker:

    def make_card(self, member_id: MemberID) -> MatchingCard:
        return MatchingCard(member_id=member_id)
