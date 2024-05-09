import uuid

from django.db import models
from django.db.models import Model
from djchoices import ChoiceItem, DjangoChoices
from model_utils.models import TimeStampedModel

from applications.member.domain_layer.value_object.enum import (
    PhotoVisibilityStatus,
)
from application.member_context.infra_layer.django.models import MemberORM
from application.meta_context.domain_layer.meta_enum import CensorStatus, PhotoType


class MemberPhotoVisibilityORM(TimeStampedModel):
    class PhotoVisibilityStatus(DjangoChoices):
        public = ChoiceItem(PhotoVisibilityStatus.PUBLIC, "공개")
        private = ChoiceItem(PhotoVisibilityStatus.PRIVATE, "비공개")

    member = models.ForeignKey(MemberORM, on_delete=models.CASCADE, related_name="photo_visibility", db_index=True)
    visibility = models.CharField(
        "사진 공개여부", choices=PhotoVisibilityStatus, blank=False, null=False, default=PhotoVisibilityStatus.public
    )

    class Meta:
        db_table = "member_photo_visibility"
        verbose_name = "[member_photo_visibility] 멤버 사진 공개 여부"
        verbose_name_plural = "[member_photo_visibility] 멤버 사진 공개 여부"

    def __str__(self) -> str:
        return f"[id: {self.id}] [member: {self.member.name}] [visibility: {self.visibility}] "


def get_s3_file_path(instance: Model, filename: str) -> str:
    file_extension = str(filename).split(".")[-1]
    path: str = f"file/{instance.member_id}/photo/{str(uuid.uuid4())[:10]}.{file_extension}"
    return path


class MemberPhotoORM(TimeStampedModel):
    class PhotoTypeChoices(DjangoChoices):
        face = ChoiceItem(PhotoType.FACE, "얼굴 사진")
        ect = ChoiceItem(PhotoType.ETC, "기타 사진")

    class PhotoCensorChoices(DjangoChoices):
        approved = ChoiceItem(CensorStatus.APPROVED, "인증 완료")
        rejected = ChoiceItem(CensorStatus.REJECTED, "인증 불가")
        under_review = ChoiceItem(CensorStatus.UNDER_CENSOR, "심사 중")

    member_id = models.PositiveBigIntegerField(db_index=True, null=False, blank=False)
    file = models.ImageField(upload_to=get_s3_file_path, blank=False, null=False)
    type = models.CharField("사진 타입", choices=PhotoTypeChoices, blank=False, null=False)
    censor_status = models.CharField("검열 상태", choices=PhotoCensorChoices, blank=False, null=False)
    is_main = models.BooleanField("대표 사진 여부", default=False, null=False, blank=False)
    is_deleted = models.BooleanField("사진 삭제 여부", default=False, null=False, blank=False)
    rejected_reason = models.CharField("검열 실패 이유", default=None, null=True, blank=False)

    class Meta:
        db_table = "member_photo"
        verbose_name = "[member_photo] 멤버 사진 정보"
        verbose_name_plural = "[member_photo] 멤버 사진 정보"

    def __str__(self) -> str:
        return f"[id: {self.id}] [is_main: {self.is_main}] [is_censored: {self.censor_status}] [file: {self.file.url}]"
