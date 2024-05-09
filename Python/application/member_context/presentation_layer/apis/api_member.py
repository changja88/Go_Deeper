from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
)
from applications.common.type import MemberID
from applications.member.domain_layer.entity.member import Member
from application.member_context.infra_layer.service.member_service import MemberService
from application.member_context.presentation_layer.apis.schemas.in_schema import (
    IntroductionChangeSchemaIn,
)
from application.member_context.presentation_layer.apis.schemas.out_schema import (
    MemberOutSchema,
)

member_router = Router()  # api_address = merry-marry.me/api/member
member_service: MemberService = MemberService()


@member_router.get(
    path="",
    response={200: MemberOutSchema},
    auth=AuthBearer(),
    summary="멤버 정보 조회",
    description="",
)
def api_get_member_info(request: Router) -> APIResponse[Member]:
    if member := member_service.find_by_member_id(member_id=MemberID(request.auth.id)):
        return member
    raise Http204NoContentException()


@member_router.put(
    path="",
    response={200: MemberOutSchema},
    auth=AuthBearer(),
    summary="멤버 소개글 변경",
    description="",
)
def api_change_member_introduction(
    request: Router, introduction_change_reqeust: IntroductionChangeSchemaIn
) -> APIResponse[Member]:
    member: Member = member_service.update_member_introduction(request.auth, introduction_change_reqeust.introduction)
    return member
