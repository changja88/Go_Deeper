from typing import Any

from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_preference_meta import (
    MemberPreferenceMeta,
)
from application.meta_context.infra_layer.service.member_preference_meta_service import (
    MemberPreferenceMetaService,
)
from application.meta_context.presentation_layer.apis.schemas.in_schema import (
    MemberPreferenceMetaSchemaIn,
)

member_preference_meta_router = Router()  # api_address = we-marry.com/api/meta/member/physical-meta


@member_preference_meta_router.get(
    path="",
    response={200: MemberPreferenceMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 기호 메타 조회",
    description="",
)
def api_find_member_preference_meta(request: Router) -> APIResponse[Any]:
    member_id = MemberID(request.auth.id)
    member_preference_meta_service: MemberPreferenceMetaService = MemberPreferenceMetaService(member_id=member_id)
    return member_preference_meta_service.find_by_memer_id(member_id=MemberID(request.auth.id))


@member_preference_meta_router.post(
    path="",
    response={201: MemberPreferenceMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 기호 메타 등록",
    description="KETWORD, GROWTH, DATE_STYLE의 경우 복수 선택이 가능함 -> meta_id_list에 여러 아이디로 등록 가능"
    "그외 의 경우 복수 선택이 불가능 함 -> meta_id_list에 한개만 보내서 등록 가능",
)
def api_register_member_physical_meta(
    request: Router,
    update_request: MemberPreferenceMetaSchemaIn,
) -> APIResponse[MemberPreferenceMeta]:
    member_id = MemberID(request.auth.id)
    member_preference_meta_service: MemberPreferenceMetaService = MemberPreferenceMetaService(member_id=member_id)
    member_preference_meta: MemberPreferenceMeta = member_preference_meta_service.register_member_preference_meta(
        member_id=MemberID(request.auth.id),
        preference_meta_id_list=update_request.meta_id_list,
        preference_meta_type=update_request.meta_type,
    )
    return 201, member_preference_meta
