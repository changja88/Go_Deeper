from applications.common.type import MemberID
from application.matching_context.domain_layer.entity.matching_exclude_friend import (
    MatchingExcludedFriendInfo,
)
from application.matching_context.domain_layer.value_object.friend import Friend


class MatchingExcludedFriendService:

    def exclude_friends_from_matching(
        self, member_id: MemberID, matching_exclude_friends: list[Friend]
    ) -> MatchingExcludedFriendInfo:
        return MatchingExcludedFriendInfo(member_id=member_id).add_matching_exclude_friends(
            friends=matching_exclude_friends
        )

    def cancel_exclude_friends_from_matching(self, member_id: MemberID) -> MatchingExcludedFriendInfo:
        return MatchingExcludedFriendInfo(member_id=member_id).remove_all_matching_exclude_friends()
