from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
)
from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.service.lookup_preference_meta_service import (
    PreferenceMetaLookupService,
)

preference_meta_lookup_router = Router()
preference_meta_lookup_service: PreferenceMetaLookupService = PreferenceMetaLookupService()


@preference_meta_lookup_router.get(
    path="", response={200: list[Meta]}, by_alias=True, summary="기호 메타 조회", description=""
)
def api_get_preference_meta(request: Router, meta_type: PreferenceMetaType) -> APIResponse[list[Meta]]:
    if preference_meta_list := preference_meta_lookup_service.find_meta_by_type(meta_type=meta_type):
        return preference_meta_list
    raise Http204NoContentException()
