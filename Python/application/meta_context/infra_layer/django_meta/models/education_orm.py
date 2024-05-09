from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.infra_layer.django_meta.models.certification_orm import (
    CertificationORM,
)


class EducationMetaPresetORM(models.Model):
    class EducationMetaTypeChoices(DjangoChoices):
        domestic = ChoiceItem(UniversityType.DOMESTIC, "국내 대학")
        international = ChoiceItem(UniversityType.INTERNATIONAL, "해외 대학")

    value = models.CharField("학교명", null=False, blank=False)
    type = models.CharField("타입", choices=EducationMetaTypeChoices.choices, blank=False, null=False, db_index=True)
    is_show = models.CharField("사용자 직접입력 값 승인여부", blank=False, null=False, default=True)
    tear = models.PositiveSmallIntegerField(null=False, default=0, help_text="평가 티어")

    class Meta:
        db_table = "education_meta_preset"
        verbose_name = "[education_meta_preset] 학력 정보 선택지"
        verbose_name_plural = "[education_meta_preset] 학력 정보 선택지"

    def __str__(self) -> str:
        return f"[id: {self.id}] [value: {self.value}]"


class MemberEducationMetaORM(CertificationORM):
    class EducationMetaTypeChoices(DjangoChoices):
        domestic = ChoiceItem(UniversityType.DOMESTIC, "국내 대학")
        international = ChoiceItem(UniversityType.INTERNATIONAL, "해외 대학")

    member_id = models.PositiveIntegerField(db_index=True, null=False, blank=False)
    education_meta = models.ForeignKey(
        EducationMetaPresetORM, on_delete=models.CASCADE, related_name="member_education_meta", blank=False, null=True
    )

    class Meta:
        db_table = "member_education_meta"
        verbose_name = "[member_education_meta] 사용자 학력 정보"
        verbose_name_plural = "[member_education_meta] 사용자 학력 계정"

    def __str__(self) -> str:
        return f"[id: {self.member_id}] [job: {self.education_meta}]"
