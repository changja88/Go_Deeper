from django.db import models
from django_extensions.db.models import TimeStampedModel

from application.member_context.infra_layer.django.models import MemberORM


class MemberWantedWeightORM(TimeStampedModel):

    member = models.ForeignKey(MemberORM, on_delete=models.CASCADE, related_name="wanted_weight", db_index=True)
    income_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    work_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    asset_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    background_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    education_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    appearance_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    birth_year_weight = models.PositiveSmallIntegerField(null=False, blank=True, default=0)

    class Meta:
        db_table = "member_wanted_weight"
        verbose_name = "[member_wanted_weight] 멤버 원티드 비중"
        verbose_name_plural = "[member_wanted_weight] 멤버 원티드 비중"

    def __str__(self) -> str:
        return (
            f"[id: {self.id}] [member_id : {self.member.id}"
            f" [appearance_weight: {self.appearance_weight}][age_weight: {self.birth_year_weight}]"
            f" [job_weight: {self.work_weight}][income_weight: {self.income_weight}]"
            f" [asset_weight: {self.asset_weight}][education_weight: {self.education_weight}]"
            f" [background_weight: {self.background_weight}]"
        )
