from django.db import models
from model_utils.models import TimeStampedModel

from application.member_context.infra_layer.django.models import MemberORM
from application.meta_context.infra_layer.django_meta.models import (
    PreferenceMetaPresetORM,
)


class MemberWantedPreferenceToPreferenceMetaPresetORM(models.Model):
    preference_meta_preset = models.ForeignKey(
        PreferenceMetaPresetORM,
        on_delete=models.CASCADE,
    )
    member_wanted_preference = models.ForeignKey(
        "MemberWantedPreferenceORM",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "member_wanted_preference_to_preference_meta_preset"
        verbose_name = "[member_wanted_preference_to_preference_meta_preset] 멤버 원티드 비중"
        verbose_name_plural = "[member_wanted_preference_to_preference_meta_preset] 멤버 원티드 비중"
        unique_together = ("preference_meta_preset", "member_wanted_preference")

    def __str__(self) -> str:
        return f"[id: {self.id}] [preference_meta_preset: {self.preference_meta_preset}]"


class MemberWantedPreferenceORM(TimeStampedModel):
    member = models.OneToOneField(
        MemberORM, on_delete=models.CASCADE, related_name="wanted_preference_set", db_index=True
    )
    preference_metas = models.ManyToManyField(
        PreferenceMetaPresetORM,
        through=MemberWantedPreferenceToPreferenceMetaPresetORM,
        through_fields=("member_wanted_preference", "preference_meta_preset"),
        related_name="wanted_preference_metas",
        blank=True,
    )

    class Meta:
        db_table = "member_wanted_preference"
        verbose_name = "[member_wanted_preference] 멤버 원티드 기호"
        verbose_name_plural = "[member_wanted_preference] 멤버 원티드 기호"

    def __str__(self) -> str:
        return f"[id: {self.id}] [member_id : {self.member.id} [preference_metas: {self.preference_metas}]"
