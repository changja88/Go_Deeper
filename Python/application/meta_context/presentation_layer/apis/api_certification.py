from ninja import Form, Router, UploadedFile
from pydantic import PositiveInt

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from application.meta_context.domain_layer.value_object.certification.meta_certification import (
    Certification,
)
from application.meta_context.infra_layer.service.certification_service import (
    CertificationService,
)
from application.meta_context.presentation_layer.apis.schemas.in_schema import (
    MetaCertificationSchemaIn,
)

certification_register_router = Router()


@certification_register_router.post(
    "",
    response={201: Certification},
    auth=AuthBearer(),
    summary="인정 정보 등록",
    description="멤버 메타 인증 자료 등록",
)
def api_register_member_certification(
    request: Router, certification_id: Form[MetaCertificationSchemaIn], files: list[UploadedFile]
) -> APIResponse[Certification]:
    return CertificationService().register_certification_files(
        files=files, certification_id=certification_id.certification_id
    )


@certification_register_router.get(
    path="",
    response={200: Certification},
    auth=AuthBearer(),
    description="멤버 메타 인증 자료 조회",
    summary="인증 정보 조회",
)
def api_get_member_certification(request: Router, certification_id: PositiveInt) -> APIResponse[Certification]:
    return CertificationService().find_by_certification_id(certification_id=certification_id)


@certification_register_router.delete(
    path="",
    response={200: Certification},
    auth=AuthBearer(),
    description="멤버 메타 인증 자료 수정",
    summary="인증 자료 삭제",
)
def api_delete_certification_file(
    request: Router, certification_id: PositiveInt, file_id: PositiveInt
) -> APIResponse[Certification]:
    return CertificationService().delete_certification_file(certification_id=certification_id, file_id=file_id)
