from itertools import islice
from typing import Optional

from applications.common.django.django_model_util import get_list_or_none
from applications.common.type import MemberID
from application.matching_context.domain_layer.value_object.friend import Friend
from application.matching_context.infra_layer.django_matching.models import (
    MatchingExcludeFriendORM,
)


class MatchingExcludeFriendWriteRepository:
    def find_all_by(self, member_id: MemberID) -> list[Friend]:
        matching_exclude_friend_list: list[Friend] = []

        matching_excluded_friends_orm: Optional[list[MatchingExcludeFriendORM]]
        matching_excluded_friends_orm = get_list_or_none(MatchingExcludeFriendORM, member_id=member_id)
        if matching_excluded_friends_orm:
            for matching_exclude_friend_orm in matching_excluded_friends_orm:
                matching_exclude_friend_list.append(
                    Friend(
                        member_id=MemberID(matching_exclude_friend_orm.member_id),
                        name=matching_exclude_friend_orm.name,
                        phone_number=matching_exclude_friend_orm.phone_number,
                    )
                )
        return matching_exclude_friend_list


class MatchingExcludeFriendReadRepository:
    def bulk_create(self, member_id: MemberID, friends: list[Friend]) -> list[Friend]:
        batch_size = 100
        matching_exclude_friend_orm_list = (
            MatchingExcludeFriendORM(member_id=member_id, name=friend.name, phone_number=friend.phone_number)
            for friend in friends
        )
        friend_list: list[Friend] = list()
        while True:
            sliced_matching_exclude_friend_orm_list = list(islice(matching_exclude_friend_orm_list, batch_size))
            if not sliced_matching_exclude_friend_orm_list:
                break
            inserted_friends_orm = MatchingExcludeFriendORM.objects.bulk_create(
                sliced_matching_exclude_friend_orm_list, batch_size, ignore_conflicts=True
            )
            friend_list.extend(
                [
                    Friend(name=friend_orm.name, phone_number=friend_orm.phone_number)
                    for friend_orm in inserted_friends_orm
                ]
            )
        return friend_list

    def delete_all(self, member_id: MemberID) -> None:
        MatchingExcludeFriendORM.objects.filter(member_id=member_id).delete()


class MatchingExcludeFriendCompoundRepository(
    MatchingExcludeFriendReadRepository, MatchingExcludeFriendWriteRepository
): ...
