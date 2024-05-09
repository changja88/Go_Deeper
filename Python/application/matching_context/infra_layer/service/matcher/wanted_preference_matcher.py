from django.utils.functional import cached_property
from pydantic import PositiveInt

from applications.common.type import MemberID
from application.matching_context.context_layer.wanted_info_request_event_pub import (
    WantedInfoRequestEventPublisher,
)
from application.wanted_context.domain_layer.value_object.wanted_preference import (
    WantedPreference,
)


class WantedPreferenceMatcher:

    target_member_id: MemberID

    @cached_property
    def member_wanted_preference(self) -> WantedPreference:
        return WantedInfoRequestEventPublisher.publish_member_wanted_info_request_event(
            member_id=self.target_member_id
        ).wanted_preference

    def __init__(self, target_member_id: MemberID) -> None:
        self.target_member_id = target_member_id

    def sort(self, other_member_ids: list[MemberID]) -> list[MemberID]:
        sorted_member_ids: list[MemberID] = sorted(
            other_member_ids,
            key=lambda other_member_id: (self.get_matched_preference_count(other_member_id), other_member_ids),
            reverse=True,
        )
        return sorted_member_ids

    def get_matched_preference_count(self, other_member_id: MemberID) -> PositiveInt:
        other_member_preference: WantedPreference = (
            WantedInfoRequestEventPublisher.publish_member_wanted_info_request_event(
                member_id=other_member_id
            ).wanted_preference
        )
        return len(self.member_wanted_preference.get_all_meta_ids() & other_member_preference.get_all_meta_ids())
