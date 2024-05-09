from typing import Any

from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from applications.member.domain_layer.entity.member_fcm import MemberFCM
from application.member_context.infra_layer.service.member_fcm_service import (
    MemberFCMService,
)
from application.meta_context.presentation_layer.apis.schemas.in_schema import (
    MemberFCMInfoSchemaIn,
)

member_fcm_router = Router()  # api_address = merry-marry.me/api/member/fcm
member_service: MemberFCMService = MemberFCMService()


@member_fcm_router.post(
    path="",
    auth=AuthBearer(),
    response={201: MemberFCM},
    summary="멤버 FCM 등록",
    description="멤버 푸시를 위한 FCM 등록 API",
)
def api_register_member_fcm_token(request: Router, fcm_info: MemberFCMInfoSchemaIn) -> APIResponse[Any]:
    member_fcm: MemberFCM = member_service.register(
        member_id=MemberID(request.auth.id), fcm_token=fcm_info.fcm_token, device_info=fcm_info.device_info
    )
    return 201, member_fcm
