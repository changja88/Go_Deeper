from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.matching_context.domain_layer.entity.matching_exclude_friend import (
    MatchingExcludedFriendInfo,
)
from application.matching_context.infra_layer.service.matching_excluded_friend_service import (
    MatchingExcludedFriendService,
)
from application.matching_context.presentation_layer.apis.schemas.in_schema import (
    MatchingExcludeFriendsSchema,
)

matching_exclude_friend_router = Router()  # api_address = we-marry.com/api/meta/lookup/education-meta


@matching_exclude_friend_router.post(
    path="friend",
    response={201: MatchingExcludedFriendInfo},
    auth=AuthBearer(),
    summary="[매칭] 지인 추천 재외",
    description="지인추천 제외 : is_exclude = true + exclude_friends"
    "지인추천 제외 취소 : is_exclude = false + exclude_friends는 생략 가능",
)
def api_matching_exclude_friend(
    request: Router, matching_exclude_friends_schema: MatchingExcludeFriendsSchema
) -> APIResponse[MatchingExcludedFriendInfo]:
    if (
        exclude_friends := matching_exclude_friends_schema.exclude_friends
    ) and matching_exclude_friends_schema.is_exclude:
        return 201, MatchingExcludedFriendService().exclude_friends_from_matching(
            member_id=MemberID(request.auth.id), matching_exclude_friends=exclude_friends
        )
    else:
        return 201, MatchingExcludedFriendService().cancel_exclude_friends_from_matching(
            member_id=MemberID(request.auth.id)
        )
