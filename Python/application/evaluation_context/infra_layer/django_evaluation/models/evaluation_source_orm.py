from django.core.validators import MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import ChoiceItem, DjangoChoices

from applications.common.enum import Gender
from application.evaluation_context.domain_layer.evaluation_enum import (
    EvaluationSourceType,
)


class EvaluationSourceORM(TimeStampedModel):

    class GenderChoices(DjangoChoices):
        female = ChoiceItem(Gender.FEMALE, "여자일 경우")
        male = ChoiceItem(Gender.MALE, "남자일 경우")

    class StandardType(DjangoChoices):
        income_source = ChoiceItem(EvaluationSourceType.INCOME_SOURCE, "소득 수준")

        job_source = ChoiceItem(EvaluationSourceType.JOB_SOURCE, "직업 수준")
        company_source = ChoiceItem(EvaluationSourceType.COMPANY_SOURCE, "회사 수준")

        asset_source = ChoiceItem(EvaluationSourceType.ASSET_SOURCE, "자산 수준")
        car_price_source = ChoiceItem(EvaluationSourceType.CAR_PRICE_SOURCE, "차량 가격(개인 자산에 포함)")

        family_asset_source = ChoiceItem(EvaluationSourceType.FAMILY_ASSET_SOURCE, "집안 자산")
        father_job_source = ChoiceItem(EvaluationSourceType.FATHER_JOB_SOURCE, "부 직업")
        mother_job_source = ChoiceItem(EvaluationSourceType.MOTHER_JOB_SOURCE, "모 직업")

        education_source = ChoiceItem(EvaluationSourceType.EDUCATION_SOURCE, "교육 수준")
        appearance_source = ChoiceItem(EvaluationSourceType.APPEARANCE_SOURCE, "외모")
        birth_year_source = ChoiceItem(EvaluationSourceType.BIRTH_YEAR_SOURCE, "나이")

    weight = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MaxValueValidator(100)],
    )
    type = models.CharField("타입", choices=StandardType.choices, blank=False, null=False)
    gender = models.CharField("성별", choices=GenderChoices.choices, blank=False, null=False)

    class Meta:
        db_table = "evaluation_source"
        verbose_name = "[evaluation_source] 사용자 평가 기준표"
        verbose_name_plural = "[evaluation_source]사용자 평가 기준표"
        unique_together = ("type", "gender")

    def __str__(self) -> str:
        return f"[id: {self.id}] [type: {self.type}] [weight: {self.weight}]"
