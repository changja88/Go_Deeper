from typing import Optional

from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
)
from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.service.lookup_finance_meta_service import (
    FinanceMetaLookupService,
)

finance_meta_lookup_router = Router()  # api_address = we-marry.com/api/meta/lookup/finance-meta
finance_meta_lookup_service: FinanceMetaLookupService = FinanceMetaLookupService()


@finance_meta_lookup_router.get(path="", response={200: list[Meta]}, description="", summary="교육 메타 조회")
def api_request_finance_meta(
    request: Router,
    meta_type: FinanceMetaType,
    search_text: Optional[str] = None,
) -> APIResponse[list[Meta]]:
    if search_text:
        return finance_meta_lookup_service.search_by(search_text=search_text, meta_type=meta_type)
    elif meta_type:
        return finance_meta_lookup_service.find_by_meta_type(meta_type=FinanceMetaType(meta_type))
    raise Http204NoContentException()
