from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from application.member_context.infra_layer.django.models import MemberORM


class MemberEvaluationORM(TimeStampedModel):
    member = models.ForeignKey(
        MemberORM,
        on_delete=models.CASCADE,
        related_name="evaluation",
        db_index=True,
        help_text="평가 대상",
    )
    work_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    income_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    asset_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    background_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    education_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    appearance_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    birth_year_point = models.DecimalField(
        null=False,
        default=0,
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        db_table = "member_evaluation"
        verbose_name = "[member_evaluation] 멤버 평가 정보"
        verbose_name_plural = "[member_evaluation] 멤버 평가 정보"
        index_together = (
            "work_point",
            "income_point",
            "asset_point",
            "background_point",
            "education_point",
            "appearance_point",
            "birth_year_point",
        )

    def __str__(self) -> str:
        return (
            f"[id: {self.id}] [member: {self.member}]"
            f" [work_point: {self.work_point}] [income_point: {self.income_point}] [asset_point: {self.asset_point}]"
            f" [background_point : {self.background_point}][education_point : {self.education_point}]"
            f" [appearance_point : {self.appearance_point}][birth_year_point : {self.birth_year_point}]"
        )
