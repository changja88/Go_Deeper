from ninja import Router

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.wanted_context.domain_layer.entity.member_wanted_info import (
    MemberWantedInfo,
)
from application.wanted_context.infra_layer.service.member_wanted_info_service import (
    MemberWantedInfoService,
    WantedPreferenceRegisterRequest,
    WantedWeightRegisterRequest,
)
from application.wanted_context.presentation_layer.apis.schemas.in_schema import (
    MemberWantedPreferenceSchemaIn,
    MemberWantedWeightSchemaIn,
)

member_wanted_router = Router()


@member_wanted_router.get(
    path="", auth=AuthBearer(), response={200: MemberWantedInfo}, summary="멤버 원티드 정보", description=""
)
def api_get_member_wanted_info(request: Router) -> APIResponse[MemberWantedInfo]:
    return MemberWantedInfoService().find_by_member_id(member_id=MemberID(request.auth.id))


@member_wanted_router.post(
    path="weight",
    auth=AuthBearer(),
    response={200: MemberWantedInfo},
    summary="멤버 비중 원티드 정보 등록",
    description="",
)
def api_register_member_wanted_info(
    request: Router, member_wanted_weight: MemberWantedWeightSchemaIn
) -> APIResponse[MemberWantedInfo]:
    return MemberWantedInfoService().register_member_wanted_weight(
        WantedWeightRegisterRequest(
            member_id=request.auth.id,
            appearance_weight=member_wanted_weight.appearance_weight,
            birth_year_weight=member_wanted_weight.birth_year_weight,
            work_weight=member_wanted_weight.work_weight,
            income_weight=member_wanted_weight.income_weight,
            asset_weight=member_wanted_weight.asset_weight,
            education_weight=member_wanted_weight.education_weight,
            background_weight=member_wanted_weight.background_weight,
        )
    )


@member_wanted_router.post(
    path="preference", auth=AuthBearer(), response={200: MemberWantedInfo}, summary="멤버 기호 원티드 정보 등록"
)
def api_register_member_wanted_preference(
    request: Router, member_wanted_preference: MemberWantedPreferenceSchemaIn
) -> APIResponse[MemberWantedInfo]:
    return MemberWantedInfoService().register_member_wanted_preference(
        WantedPreferenceRegisterRequest(
            member_id=request.auth.id,
            meta_ids=member_wanted_preference.meta_ids,
            preference_type=member_wanted_preference.preference_type,
        )
    )
