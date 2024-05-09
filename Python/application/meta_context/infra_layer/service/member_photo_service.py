from typing import Optional

from ninja import File, UploadedFile
from pydantic import BaseModel, StrictBool

from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_photo_meta import (
    MemberPhotoMeta,
)
from application.meta_context.domain_layer.meta_enum import PhotoType
from application.meta_context.domain_layer.value_object.meta.photo import Photo


class PhotoAddRequest(BaseModel):
    file: File[UploadedFile]
    member_id: MemberID
    photo_type: PhotoType
    is_main: StrictBool


class MemberPhotoUpdateRequest(BaseModel):
    photo_id: int
    member_id: MemberID
    is_main: Optional[StrictBool]
    is_deleted: Optional[StrictBool]


class MemberPhotoService:
    def find_by(self, member_id: MemberID) -> MemberPhotoMeta:
        return MemberPhotoMeta(member_id=member_id)

    def add_photo(self, photo_add_request: PhotoAddRequest) -> MemberPhotoMeta:
        photo: Photo = Photo(
            file=photo_add_request.file,
            type=photo_add_request.photo_type,
            is_main=photo_add_request.is_main,
        )

        member_photo: MemberPhotoMeta = MemberPhotoMeta(member_id=photo_add_request.member_id)
        member_photo.add_photo(new_photo=photo)
        return member_photo

    def update_photo(self, update_photo_reqeust: MemberPhotoUpdateRequest) -> MemberPhotoMeta:
        member_photo: MemberPhotoMeta = MemberPhotoMeta(member_id=update_photo_reqeust.member_id)
        member_photo.set_photo_attrs(
            photo_id=update_photo_reqeust.photo_id,
            is_main=update_photo_reqeust.is_main,
            is_deleted=update_photo_reqeust.is_deleted,
        )
        return member_photo
