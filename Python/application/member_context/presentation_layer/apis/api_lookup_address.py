from typing import Optional

from ninja import Router

from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
)
from application.member_context.infra_layer.service.address_lookup_service import (
    AddressLookupService,
)
from application.member_context.presentation_layer.apis.schemas.out_schema import (
    AddressLookupOutSchema,
)

address_lookup_router = Router()  # api_address = merry-marry.me/api/member/address-lookup/
address_lookup_service: AddressLookupService = AddressLookupService()


@address_lookup_router.get(
    path="",
    response={200: AddressLookupOutSchema},
    by_alias=True,
    summary="주소 조회",
    description="",
)
def api_find_member_by(request: Router, lv1_id: Optional[int] = None) -> APIResponse[AddressLookupOutSchema]:
    if address_list := address_lookup_service.find_all_address(lv1_id=lv1_id):
        return AddressLookupOutSchema(address_list=address_list)
    raise Http204NoContentException()
