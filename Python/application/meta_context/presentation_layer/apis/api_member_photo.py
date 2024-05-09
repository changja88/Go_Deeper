from ninja import File, Form, Router, UploadedFile

from applications.common.ninja.authentication import AuthBearer
from applications.common.ninja.custom_type import APIResponse
from applications.common.type import MemberID
from application.member_context.presentation_layer.apis.schemas.in_schema import (
    MemberPhotoRegisterSchemaIn,
    MemberPhotoUpdateSchemaIn,
)
from application.member_context.presentation_layer.apis.schemas.out_schema import (
    MemberPhotoOutSchema,
)
from application.meta_context.domain_layer.entity.member_photo_meta import (
    MemberPhotoMeta,
)
from application.meta_context.infra_layer.service.member_photo_service import (
    MemberPhotoService,
    MemberPhotoUpdateRequest,
    PhotoAddRequest,
)

member_photo_router = Router()  # api_address = merry-marry.me/api/meta/photo/
photo_service: MemberPhotoService = MemberPhotoService()


@member_photo_router.get(
    path="",
    response={200: MemberPhotoOutSchema},
    auth=AuthBearer(),
    by_alias=True,
    summary="멤버 사진 조회",
    description="",
)
def api_get_member_photo(request: Router) -> APIResponse[MemberPhotoMeta]:
    return photo_service.find_by(MemberID(request.auth.id))


@member_photo_router.post(
    path="", response={201: MemberPhotoMeta}, auth=AuthBearer(), description="", summary="멤버 사진 등록"
)
def api_register_member_photo(
    request: Router, add_photo_reqeust: Form[MemberPhotoRegisterSchemaIn], file: File[UploadedFile]
) -> APIResponse[MemberPhotoMeta]:
    return photo_service.add_photo(
        PhotoAddRequest(
            file=file,
            member_id=MemberID(request.auth.id),
            photo_type=add_photo_reqeust.photo_type,
            is_main=add_photo_reqeust.is_main,
        )
    )


@member_photo_router.put(
    path="", response={201: MemberPhotoMeta}, auth=AuthBearer(), summary="멤버 사진 수정", description=""
)
def api_update_member_photo(
    request: Router, update_photo_request: MemberPhotoUpdateSchemaIn
) -> APIResponse[MemberPhotoMeta]:
    member_photo_update_reqeust: MemberPhotoUpdateRequest = MemberPhotoUpdateRequest(
        member_id=MemberID(request.auth.id), **update_photo_request.model_dump()
    )
    member_photo: MemberPhotoMeta = photo_service.update_photo(member_photo_update_reqeust)
    return member_photo
