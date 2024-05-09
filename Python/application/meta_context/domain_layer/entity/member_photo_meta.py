from typing import Annotated, Optional

from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from applications.member.domain_layer.value_object.enum import (
    PhotoVisibilityStatus,
)
from application.meta_context.domain_layer.value_object.meta.photo import Photo
from application.meta_context.infra_layer.repository.member_photo_repositories import (
    MemberPhotoCompoundRepository,
)


class MemberPhotoMeta(ValueObject):
    member_id: MemberID
    photos: Annotated[list[Photo], Field(default_factory=list)]
    visibility: PhotoVisibilityStatus
    repo: SkipJsonSchema[MemberPhotoCompoundRepository] = Field(exclude=True)

    def __init__(self, member_id: MemberID, repo: MemberPhotoCompoundRepository = MemberPhotoCompoundRepository()):
        visibility: Optional[PhotoVisibilityStatus] = repo.find_member_photo_visibility_status_by(member_id=member_id)
        if not visibility:
            repo.register_photo_visibility(member_id=member_id)
        super().__init__(
            member_id=member_id,
            visibility=visibility,
            photos=repo.find_member_photo_list_by(member_id=member_id),
            repo=repo,
        )

    def find_main_photo(self) -> Optional[Photo]:
        for photo in self.photos:
            if photo.is_main:
                return photo
        return None

    def add_photo(self, new_photo: Photo) -> None:
        photo: Photo = self.repo.create_photo(member_id=MemberID(self.member_id), photo=new_photo)
        self.photos.append(photo)

    def set_visibility(self, visibility: PhotoVisibilityStatus) -> None:
        self.repo.register_photo_visibility(member_id=MemberID(self.member_id), visibility=visibility)
        self.visibility = visibility

    def _get_photo_by(self, photo_id: int) -> Optional[Photo]:
        for photo in self.photos:
            return photo if photo.id == photo_id else None
        return None

    def set_photo_attrs(
        self,
        photo_id: int,
        is_main: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
    ) -> None:
        def _set_all_photos_is_main_as_false() -> None:
            for member_photo in self.photos:
                member_photo.set_is_main_as(False)
                self.repo.update(member_id=MemberID(self.member_id), photo=member_photo)

        if photo := self._get_photo_by(photo_id=photo_id):
            if is_main is not None:
                if is_main:
                    _set_all_photos_is_main_as_false()
                photo.set_is_main_as(is_main)
            if is_deleted is not None:
                photo.set_is_delete_as(is_deleted)

            self.repo.update(member_id=MemberID(self.member_id), photo=photo)
