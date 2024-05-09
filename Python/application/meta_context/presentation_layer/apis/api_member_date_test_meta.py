from typing import Any

from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_date_test_meta import (
    MemberDateTestMeta,
)
from application.meta_context.infra_layer.service.member_date_test_meta_service import (
    MemberDateTestMetaService,
    MemberDateTestResponse,
)

member_date_test_meta_lookup_router = Router()  # api_address = we-marry.com/api/meta/lookup/education-meta
member_date_test_service: MemberDateTestMetaService = MemberDateTestMetaService()


@member_date_test_meta_lookup_router.get(
    path="",
    response={200: MemberDateTestMeta},
    auth=AuthBearer(),
    description="",
    summary="멤버 데이트 설문지 메타 조회",
)
def api_get_member_date_test(request: Router) -> APIResponse[MemberDateTestMeta]:
    return member_date_test_service.find_by(member_id=MemberID(request.auth.id))


@member_date_test_meta_lookup_router.post(
    path="",
    response={201: MemberDateTestMeta},
    auth=AuthBearer(),
    description="",
    summary="멤버 데이트 설문지 메타 등록",
)
def api_register_member_date_test_response(
    request: Router, member_response: MemberDateTestResponse
) -> APIResponse[Any]:
    member_date_test_answer: MemberDateTestMeta = member_date_test_service.register_member_date_test_response(
        member_id=MemberID(request.auth.id), response=member_response
    )
    return 201, member_date_test_answer
