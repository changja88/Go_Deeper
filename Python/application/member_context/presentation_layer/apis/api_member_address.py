from typing import Optional

from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.ninja.response.exception.exception_response import (
    Http204NoContentException,
)
from applications.common.type import MemberID
from applications.member.domain_layer.entity.member_address import MemberAddress
from applications.member.domain_layer.value_object.address import AddressIdSet
from application.member_context.infra_layer.service.member_address_service import (
    MemberAddressService,
)
from application.member_context.presentation_layer.apis.schemas.out_schema import (
    MemberAddressOutSchema,
)

member_address_router = Router()  # api_address = merry-marry.me/api/member/address/
member_address_service: MemberAddressService = MemberAddressService()


@member_address_router.get(
    path="",
    response={200: MemberAddressOutSchema},
    summary="멤버 주소 조회",
    auth=AuthBearer(),
)
def get_member_address(request: Router) -> APIResponse[MemberAddress]:
    if member_address := member_address_service.find_by_id(MemberID(request.auth.id)):
        return member_address
    raise Http204NoContentException()


@member_address_router.post(
    path="",
    response={201: MemberAddress},
    auth=AuthBearer(),
    summary="멤버 주소 등록",
    description="API 변경 사항" "- member_address안에 living_address, playing_address가 있었는데 밖으로 뻇습니다",
)
def api_create_member_address(
    request: Router, playing_address: Optional[AddressIdSet] = None, living_address: Optional[AddressIdSet] = None
) -> APIResponse[MemberAddress]:
    member_address: MemberAddress
    if playing_address:
        member_address = member_address_service.register_member_playing_address(
            member_id=MemberID(request.auth.id), address_id_set=playing_address
        )
    if living_address:
        member_address = member_address_service.register_member_living_address(
            member_id=MemberID(request.auth.id), address_id_set=living_address
        )

    return 201, member_address


@member_address_router.put(
    path="",
    response={201: MemberAddress},
    auth=AuthBearer(),
    summary="멤버 주소 변경",
    description="변경하고 싶은 것만 넣어줘도 됩니다",
)
def api_update_member_address(
    request: Router, playing_address: Optional[AddressIdSet] = None, living_address: Optional[AddressIdSet] = None
) -> APIResponse[MemberAddress]:
    member_address: MemberAddress
    if playing_address:
        member_address = member_address_service.register_member_playing_address(
            member_id=MemberID(request.auth.id), address_id_set=playing_address
        )
    if living_address:
        member_address = member_address_service.register_member_living_address(
            member_id=MemberID(request.auth.id), address_id_set=living_address
        )

    return 201, member_address
