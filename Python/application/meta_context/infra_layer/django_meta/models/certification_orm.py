import uuid

from django.db import models
from django.db.models import Model
from django_extensions.db.models import TimeStampedModel
from djchoices import ChoiceItem, DjangoChoices

from application.meta_context.domain_layer.meta_enum import CensorStatus


class CertificationORM(TimeStampedModel):

    class CensorStatusChoices(DjangoChoices):
        under_censor = ChoiceItem(CensorStatus.UNDER_CENSOR, "심사중")
        approved = ChoiceItem(CensorStatus.APPROVED, "심사 완료")
        rejected = ChoiceItem(CensorStatus.REJECTED, "심사 거절")

    censor_status = models.CharField(
        "심사 결과",
        choices=CensorStatusChoices.choices,
        blank=False,
        null=False,
        db_index=True,
        default=CensorStatusChoices.under_censor,
    )

    rejected_reason = models.CharField("검열 실패 이유", default=None, null=True, blank=False)

    class Meta:
        db_table = "certification"
        verbose_name = "[certification] 사용자 신체 메타 정보"
        verbose_name_plural = "[certification] 사용자 신체 메타 정보"

    def __str__(self) -> str:
        return f"[id: {self.id}] [censor_status: {self.censor_status}] [rejected_reason: {self.rejected_reason}]"


def get_s3_cerification_file_path(instance: Model, filename: str) -> str:
    file_extension = str(filename).split(".")[-1]
    path: str = f"file/certification/{str(uuid.uuid4())[:10]}.{file_extension}"
    # path: str = f"file/{instance.member_id}/certification/{str(uuid.uuid4())[:10]}.{file_extension}"
    return path


class CertificationFileORM(TimeStampedModel):
    file = models.FileField(upload_to=get_s3_cerification_file_path, blank=False, null=False)
    certification = models.ForeignKey(
        CertificationORM, on_delete=models.CASCADE, related_name="certification_file", blank=False, null=True
    )
    is_deleted = models.BooleanField(blank=False, null=False, default=False)

    class Meta:
        db_table = "certification_file"
        verbose_name = "[certification_file] 멤버 메타 인증"
        verbose_name_plural = "[certification_file] 멤버 메타 인증"

    def __str__(self) -> str:
        return f"[id: {self.id}] [files: {self.file}]"
