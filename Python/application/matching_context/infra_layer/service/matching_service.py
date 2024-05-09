from applications.common.type import MemberID
from application.matching_context.domain_layer.entity.matching_exclude_friend import (
    MatchingExcludedFriendInfo,
)
from application.matching_context.domain_layer.value_object.matching_card import (
    MatchingCard,
)
from application.matching_context.infra_layer.service.helper.matching_card_maker import (
    MatchingCardMaker,
)
from application.matching_context.infra_layer.service.matcher.date_test_matcher import (
    DateTestMatcher,
)
from application.matching_context.infra_layer.service.matcher.wanted_preference_matcher import (
    WantedPreferenceMatcher,
)
from application.matching_context.infra_layer.service.matcher.wanted_weight_matcher import (
    WantedWeightMatcher,
)


class MatchingService:

    target_member_id: MemberID
    wanted_weight_matcher: WantedWeightMatcher
    wanted_preference_matcher: WantedPreferenceMatcher
    date_test_matcher: DateTestMatcher = DateTestMatcher(similarity_threshold=0)
    matching_card_maker: MatchingCardMaker = MatchingCardMaker()

    def __init__(self, target_member_id: MemberID):
        self.target_member_id = target_member_id
        self.wanted_weight_matcher = WantedWeightMatcher(member_id=target_member_id)
        self.wanted_preference_matcher = WantedPreferenceMatcher(target_member_id=target_member_id)

    def match(self) -> MatchingCard:
        # 원티드 비중 반영
        matched_members: list[MemberID] = self.wanted_weight_matcher.find_matched_member_list()
        # 제외 친구 반영
        matched_members = self._exclude_excluded_friends(
            target_member_id=self.target_member_id,
            matched_member_ids=matched_members,
        )
        # 가치관 반영(데이트 테스트)
        matched_members = self.date_test_matcher.find_matched_member_list(
            target_member_id=self.target_member_id,
            other_member_ids=matched_members,
        )
        # 원티드 기호 반영(정렬)
        matched_members = self.wanted_preference_matcher.sort(other_member_ids=matched_members)
        return self.matching_card_maker.make_card(member_id=matched_members[0])

    def _exclude_excluded_friends(
        self, target_member_id: MemberID, matched_member_ids: list[MemberID]
    ) -> list[MemberID]:
        return [
            matched_member_id
            for matched_member_id in matched_member_ids
            if matched_member_id
            not in MatchingExcludedFriendInfo(member_id=target_member_id).find_all_excluded_friends()
        ]
