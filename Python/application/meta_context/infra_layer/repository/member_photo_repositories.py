from typing import Any, Optional

from django.forms import model_to_dict

from applications.common.django.django_model_util import (
    get_list_or_none,
    get_obj_or_none,
)
from applications.common.type import MemberID
from applications.member.domain_layer.value_object.enum import (
    PhotoVisibilityStatus,
)
from application.meta_context.domain_layer.value_object.meta.photo import Photo
from application.meta_context.infra_layer.django_meta.models.member_photo_orm import (
    MemberPhotoORM,
    MemberPhotoVisibilityORM,
)


class MemberPhotoReadRepository:
    def find_member_photo_visibility_status_by(self, member_id: MemberID) -> Optional[PhotoVisibilityStatus]:
        member_photo_visibility_orm: Optional[MemberPhotoVisibilityORM] = get_obj_or_none(
            MemberPhotoVisibilityORM, member_id=member_id
        )
        if member_photo_visibility_orm:
            return PhotoVisibilityStatus(member_photo_visibility_orm.visibility)
        return None

    def find_member_photo_list_by(self, member_id: MemberID) -> list[Photo]:
        photo_list: list[Photo] = list()
        if member_photo_orm_list := get_list_or_none(MemberPhotoORM, member_id=member_id):
            for member_photo_orm in member_photo_orm_list:
                snap_shot: dict[str, Any] = model_to_dict(member_photo_orm)
                snap_shot.pop("file")
                photo: Photo = Photo(
                    file=member_photo_orm.file.url,
                    **snap_shot,
                )
                photo_list.append(photo)
        return photo_list


class MemberPhotoWriteRepository:
    def create_photo(self, member_id: MemberID, photo: Photo) -> Photo:
        data = photo.model_dump()
        member_photo_orm: MemberPhotoORM = MemberPhotoORM.objects.create(member_id=member_id, **data)
        snap_shot: dict[str, Any] = model_to_dict(member_photo_orm)
        snap_shot.pop("file")
        return Photo(file=member_photo_orm.file.url, **snap_shot)

    def register_photo_visibility(
        self, member_id: MemberID, visibility: PhotoVisibilityStatus = PhotoVisibilityStatus.PUBLIC
    ) -> None:
        MemberPhotoVisibilityORM.objects.update_or_create(member_id=member_id, defaults={"visibility": visibility})

    def update(self, member_id: MemberID, photo: Photo) -> Photo:
        data = photo.model_dump()
        # 사진 교체는 불가능함 + 사진 저장 이름은 랜덤으로 만들어지기 때문에 항상 업데이트가 되므로 하면 안됨
        data.pop("file")
        member_photo_orm, updated = MemberPhotoORM.objects.update_or_create(
            member_id=member_id, id=photo.id, defaults=data
        )
        snap_shot: dict[str, Any] = model_to_dict(member_photo_orm)
        snap_shot.pop("file")
        return Photo(file=member_photo_orm.file.url, **snap_shot)


class MemberPhotoCompoundRepository(MemberPhotoReadRepository, MemberPhotoWriteRepository): ...
