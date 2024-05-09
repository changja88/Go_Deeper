from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from application.meta_context.domain_layer.meta_enum import PhysicalMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.service.lookup_physical_meta_service import (
    PhysicalMetaLookupService,
)

physical_meta_lookup_router = Router()  # api_address = merry-marry.me/api/meta/lookup/physical-meta
physical_meta_lookup_service: PhysicalMetaLookupService = PhysicalMetaLookupService()


@physical_meta_lookup_router.get(
    path="",
    response={200: list[Meta]},
    by_alias=True,
    summary="신체 메타 조회",
    description="",
)
def api_get_member_photo(request: Router, meta_type: PhysicalMetaType) -> APIResponse[list[Meta]]:
    return physical_meta_lookup_service.find_meta_by_type(meta_type)
