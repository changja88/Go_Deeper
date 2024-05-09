from typing import Optional

from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
)
from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.service.lookup_education_meta_service import (
    EducationMetaLookupService,
)

education_meta_lookup_router = Router()  # api_address = we-marry.com/api/meta/lookup/education-meta
education_meta_lookup_service: EducationMetaLookupService = EducationMetaLookupService()


@education_meta_lookup_router.get(
    path="", response={200: list[Meta]}, by_alias=True, summary="교육 메타 조회", description=""
)
def api_get_education_meta_list(
    request: Router, meta_type: UniversityType, search_text: Optional[str] = None
) -> APIResponse[list[Meta]]:
    if search_text:
        if result := education_meta_lookup_service.search_by(meta_type=meta_type, search_text=search_text):
            return result
    else:
        if result := education_meta_lookup_service.find_all_by_meta_type(meta_type=meta_type):
            return result
    raise Http204NoContentException()
