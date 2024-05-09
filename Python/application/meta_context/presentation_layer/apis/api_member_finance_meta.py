from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_finance_meta import (
    MemberFinanceMeta,
)
from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.infra_layer.service.member_finance_meta_service import (
    MemberFinanceMetaService,
)
from application.meta_context.presentation_layer.apis.schemas.in_schema import (
    MemberCustomMetaSchemaIn,
    MemberMetaSchemaIn,
    MemberMultipleMetaSchemaIn,
)

member_finance_meta_router = Router()  # api_address = we-marry.com/api/meta/member/finance-meta
member_finance_meta_service: MemberFinanceMetaService = MemberFinanceMetaService()


@member_finance_meta_router.get(
    path="", response={200: MemberFinanceMeta}, auth=AuthBearer(), summary="멤버 경제력 메타 조회", description=""
)
def api_find_member_finance_meta(request: Router) -> APIResponse[MemberFinanceMeta]:
    return member_finance_meta_service.find_by_member_id(member_id=MemberID(request.auth.id))


@member_finance_meta_router.post(
    path="/custom",
    response={201: MemberFinanceMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 경제력 메타 직접입력 등록",
    description="",
)
def api_register_custom_member_finance_meta(
    request: Router, custom_meta: MemberCustomMetaSchemaIn
) -> APIResponse[MemberFinanceMeta]:
    member_finance_meta: MemberFinanceMeta = member_finance_meta_service.register_custom_member_finance_meta(
        member_id=request.auth.id,
        meta_type=FinanceMetaType(custom_meta.meta_type),
        custom_value=custom_meta.custom_value,
    )
    return 201, member_finance_meta


@member_finance_meta_router.post(
    path="",
    response={201: MemberFinanceMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 경제력 메타 등록",
    description="",
)
def api_register_member_finance_meta(
    request: Router,
    member_meta_id: MemberMetaSchemaIn,
) -> APIResponse[MemberFinanceMeta]:
    member_finance_meta: MemberFinanceMeta = member_finance_meta_service.register_member_finance_meta(
        member_id=request.auth.id, meta_id=member_meta_id.meta_id
    )
    return 201, member_finance_meta


@member_finance_meta_router.post(
    path="list",
    response={201: MemberFinanceMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 경제력 메타 복수개 등록",
    description="메터 복수개 등록",
)
def api_register_member_finance_meta_list(
    request: Router, member_meta_requests: MemberMultipleMetaSchemaIn
) -> APIResponse[MemberFinanceMeta]:
    member_finance_meta: MemberFinanceMeta
    for member_meta_id in member_meta_requests.meta_id_list:
        member_finance_meta = member_finance_meta_service.register_member_finance_meta(
            member_id=request.auth.id, meta_id=member_meta_id
        )
    return 201, member_finance_meta
