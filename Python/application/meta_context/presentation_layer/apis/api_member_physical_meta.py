from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_physical_meta import (
    MemberPhysicalMeta,
)
from application.meta_context.infra_layer.service.member_physical_meta_service import (
    MemberPhysicalMetaInput,
    MemberPhysicalMetaService,
)
from application.meta_context.presentation_layer.apis.schemas.in_schema import (
    MemberMetaSchemaIn,
)

member_physical_meta_router = Router()  # api_address = we-marry.com/api/meta/member/physical-meta
member_physical_meta_service: MemberPhysicalMetaService = MemberPhysicalMetaService()


@member_physical_meta_router.get(
    path="",
    response={200: MemberPhysicalMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 신체 메타 조회",
    description="",
)
def api_find_member_physical_meta(request: Router) -> APIResponse[MemberPhysicalMeta]:
    member_physical_meta_service: MemberPhysicalMetaService = MemberPhysicalMetaService()
    return member_physical_meta_service.find_by_member_id(member_id=MemberID(request.auth.id))


@member_physical_meta_router.post(
    path="",
    response={201: MemberPhysicalMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 신체 메타 등록",
    description="업데이트가 필요없는 메타는 값에 null을 보내주시면 됩니다",
)
def api_register_member_physical_meta(
    request: Router, update_request: MemberMetaSchemaIn
) -> APIResponse[MemberPhysicalMeta]:
    member_physical_meta_service: MemberPhysicalMetaService = MemberPhysicalMetaService()
    member_physical_meta = member_physical_meta_service.update_member_physical_meta(
        update_request=MemberPhysicalMetaInput(member_id=MemberID(request.auth.id), meta_id=update_request.meta_id)
    )
    return 201, member_physical_meta
