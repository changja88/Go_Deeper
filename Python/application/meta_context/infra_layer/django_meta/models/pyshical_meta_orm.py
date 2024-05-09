from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import ChoiceItem, DjangoChoices

from application.member_context.infra_layer.django.models import MemberORM
from application.meta_context.domain_layer.meta_enum import PhysicalMetaType


class PhysicalMetaPresetORM(models.Model):
    class PhysicalMetaTypeChoices(DjangoChoices):
        body_shape = ChoiceItem(PhysicalMetaType.BODY_SHAPE, "체형")
        weight = ChoiceItem(PhysicalMetaType.HEIGHT, "체중")
        height = ChoiceItem(PhysicalMetaType.WEIGHT, "키")

    value = models.CharField("타입에 해당하는 값", null=False, blank=False)
    type = models.CharField("타입", choices=PhysicalMetaTypeChoices.choices, blank=False, null=False, db_index=True)

    class Meta:
        db_table = "physical_meta_preset"
        verbose_name = "[physical_meta_preset] 신체 정보 선택지"
        verbose_name_plural = "[physical_meta_preset] 신체 정보 선택지"

    def __str__(self) -> str:
        return f"[id: {self.id}] [type: {self.type}] [value: {self.value}]"


class MemberPhysicalMetaORM(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(MemberORM, on_delete=models.CASCADE, related_name="physical_meta", db_index=True)
    physical_meta = models.ForeignKey(
        PhysicalMetaPresetORM, on_delete=models.CASCADE, related_name="member_physical_meta", blank=False, null=True
    )

    class Meta:
        db_table = "member_physical_meta"
        verbose_name = "[member_physical_meta] 사용자 신체 메타 정보"
        verbose_name_plural = "[member_physical_meta] 사용자 신체 메타 정보"

    def __str__(self) -> str:
        return f"[id: {self.id}] [physical_meta: {self.physical_meta}]"
