from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.matching_context.domain_layer.value_object.matching_card import (
    MatchingCard,
)
from application.matching_context.infra_layer.service.matching_service import (
    MatchingService,
)

matching_router = Router()  # api_address = we-marry.com/api/meta/lookup/education-meta


@matching_router.get(
    path="",
    response={200: MatchingCard},
    auth=AuthBearer(),
    summary="[매칭] 임으로 해당 유저의 매칭 조회",
    description="테스트용으로 사용가능 합니다",
)
def api_match_member(request: Router) -> APIResponse[MatchingCard]:
    a = MatchingService(MemberID(request.auth.id)).match()
    return a
