from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
    Http400BadRequestException,
)
from applications.common.type import MemberID
from application.member_context.context_layer.publisher.register_event_pub import (
    RegisterEventPublisher,
)
from applications.member.domain_layer.entity.member import Member
from applications.member.domain_layer.value_object.unique_info import UniqueInfo
from application.member_context.infra_layer.django.models import BearerTokenORM
from application.member_context.infra_layer.repository.member_repositories import (
    MemberFindCondition,
)
from application.member_context.infra_layer.service.register_service import (
    RegisterService,
)
from application.member_context.infra_layer.service.token_service import TokenService
from application.member_context.presentation_layer.apis.schemas.in_schema import (
    RegistrationSchemaIn,
)
from application.member_context.presentation_layer.apis.schemas.out_schema import (
    BearerTokenOutSchema,
)

# api_address = merry-marry.me/api/member/register

register_router = Router()


@register_router.post(path="", response={201: BearerTokenOutSchema}, by_alias=True, summary="회원 가입", description="")
def api_register_member(request: Router, register_info: RegistrationSchemaIn) -> APIResponse[BearerTokenORM]:
    member: Member = RegisterService().register(
        unique_info=UniqueInfo(
            name=register_info.name, phone_number=register_info.phone_number, nickname=register_info.nickname
        )
    )
    if member_id := member.id:
        token: BearerTokenORM = TokenService().register_by(member_id=MemberID(member.id))
        RegisterEventPublisher.publish_birth_year_register_event(
            member_id=MemberID(member_id), birth_year=register_info.birth_year, gender=register_info.gender
        )
        return 201, token
    raise Http400BadRequestException()


@register_router.get(
    path="",
    response={200: BearerTokenOutSchema},
    summary="기가입자 토큰 획득용 (전화번호, 이름, 생년원일이 모두 같아야함)",
    description="",
)
def api_get_existing_member(request: Router, phone_number: str, name: str) -> APIResponse[BearerTokenORM]:
    if member := RegisterService().find_by_cond(find_cond=MemberFindCondition(name=name, phone_number=phone_number)):
        if member_id := member.id:
            token: BearerTokenORM = TokenService().find_token_by(member_id=MemberID(member_id))
            return token
    raise Http204NoContentException()
