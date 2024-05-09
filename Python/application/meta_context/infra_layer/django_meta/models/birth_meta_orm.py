from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import ChoiceItem, DjangoChoices

from applications.common.enum import Gender
from application.member_context.infra_layer.django.models import MemberORM


class MemberBirthMetaORM(TimeStampedModel):

    class GenderChoices(DjangoChoices):
        female = ChoiceItem(Gender.FEMALE, "여자")
        male = ChoiceItem(Gender.MALE, "남자")

    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(MemberORM, on_delete=models.CASCADE, related_name="birth_meta", db_index=True)
    birth_year = models.PositiveIntegerField(blank=False, null=False)
    gender = models.CharField("성별", choices=GenderChoices.choices, blank=False, null=False)

    class Meta:
        db_table = "member_birth_meta"
        verbose_name = "[member_birth_meta] 사용자 출생 메타 정보"
        verbose_name_plural = "[member_birth_meta] 사용자 출생 메타 정보"

    def __str__(self) -> str:
        return f"[id: {self.member_id}] [birth_year: {self.birth_year}] [gender: {self.gender}]"
