from typing import Any

from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_education_meta import (
    MemberEducationMeta,
)
from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.infra_layer.service.member_education_meta_service import (
    MemberEducationMetaService,
)
from application.meta_context.presentation_layer.apis.schemas.in_schema import (
    MemberCustomMetaSchemaIn,
    MemberMetaSchemaIn,
)

member_education_meta_router = Router()  # api_address = we-marry.com/api/meta/member/education-meta
member_education_meta_service: MemberEducationMetaService = MemberEducationMetaService()


@member_education_meta_router.post(
    path="",
    response={201: MemberEducationMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 교육 메타 등록",
    description="",
)
def api_register_member_education_meta(request: Router, education_meta_request: MemberMetaSchemaIn) -> APIResponse[Any]:
    member_education_meta: MemberEducationMeta = member_education_meta_service.register_member_education_meta(
        meta_id=education_meta_request.meta_id,
        member_id=MemberID(request.auth.id),
    )
    return 201, member_education_meta


@member_education_meta_router.post(
    path="/custom",
    response={201: MemberEducationMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 교육 메타 직접입력 등록",
    description="",
)
def api_register_custom_member_education_meta(
    request: Router, education_meta_request: MemberCustomMetaSchemaIn
) -> APIResponse[Any]:
    member_education_meta: MemberEducationMeta = member_education_meta_service.register_member_custom_education_meta(
        meta_type=UniversityType(education_meta_request.meta_type),
        custom_value=education_meta_request.custom_value,
        member_id=MemberID(request.auth.id),
    )
    return 201, member_education_meta


@member_education_meta_router.get(
    path="",
    response={200: MemberEducationMeta},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 교육 메타 조회",
    description="",
)
def api_get_member_education_meta(request: Router) -> APIResponse[MemberEducationMeta]:
    return MemberEducationMeta(member_id=MemberID(request.auth.id))
