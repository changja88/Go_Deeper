from ninja import Router
from pydantic import StrictBool

from applications.common.ninja.custom_type import APIResponse
from application.member_context.infra_layer.service.register_service import (
    RegisterService,
)
from application.member_context.presentation_layer.apis.schemas.out_schema import (
    MemberDuplicationOutSchema,
)

nick_name_router = Router()  # api_address = merry-marry.me/api/member/nickname
member_service: RegisterService = RegisterService()


@nick_name_router.get(
    path="",
    response={200: MemberDuplicationOutSchema},
    summary="닉네임 중복 조회",
    description="닉네임이 중복인 경우에도 200으로 리턴 합니다. 필드 값으로 중복여부로 확인해야 합니다",
)
def api_nick_name_duplication_check(request: Router, nickname: str) -> APIResponse[MemberDuplicationOutSchema]:
    is_exists: StrictBool = member_service.is_nickname_exists(nickname=nickname)
    return MemberDuplicationOutSchema(is_able=not is_exists)
