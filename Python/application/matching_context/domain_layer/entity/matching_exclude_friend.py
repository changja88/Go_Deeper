from typing import Self

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.matching_context.domain_layer.value_object.friend import Friend
from application.matching_context.infra_layer.repository.matching_exclude_friend_repositories import (
    MatchingExcludeFriendCompoundRepository,
)


class MatchingExcludedFriendInfo(ValueObject):
    member_id: MemberID
    friends: list[Friend]
    repo: SkipJsonSchema[MatchingExcludeFriendCompoundRepository] = Field(exclude=True)

    def __init__(
        self,
        member_id: MemberID,
        repo: MatchingExcludeFriendCompoundRepository = MatchingExcludeFriendCompoundRepository(),
    ):
        super().__init__(member_id=member_id, friends=repo.find_all_by(member_id=member_id), repo=repo)

    def add_matching_exclude_friends(self, friends: list[Friend]) -> Self:
        self.remove_all_matching_exclude_friends()
        self.friends = self.repo.bulk_create(friends=friends, member_id=self.member_id)
        return self

    def remove_all_matching_exclude_friends(self) -> Self:
        self.repo.delete_all(member_id=self.member_id)
        self.friends.clear()
        return self

    def find_all_excluded_friends(self) -> list[MemberID]:
        return [friend.member_id for friend in self.friends]
