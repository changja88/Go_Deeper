from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from application.meta_context.domain_layer.value_object.meta.date_test import DateTest
from application.meta_context.infra_layer.service.lookup_date_test_meta_service import (
    DateTestMetaLookupService,
)

date_test_meta_lookup_router = Router()  # api_address = we-marry.com/api/meta/lookup/education-meta


@date_test_meta_lookup_router.get(path="", response={200: DateTest}, summary="데이트 설문지 메타 조회", description="")
def api_get_date_test_meta(request: Router) -> APIResponse[DateTest]:
    return DateTestMetaLookupService().find_all()
