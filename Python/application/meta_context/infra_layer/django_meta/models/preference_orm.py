from django.db import models
from django_extensions.db.models import TimeStampedModel
from djchoices import ChoiceItem, DjangoChoices

from application.meta_context.domain_layer.meta_enum import PreferenceMetaType


class PreferenceMetaPresetORM(models.Model):
    class PreferenceMetaTypeChoices(DjangoChoices):
        job = ChoiceItem(PreferenceMetaType.SMOKING, "흡연")
        income = ChoiceItem(PreferenceMetaType.ALCOHOL, "음주")
        company = ChoiceItem(PreferenceMetaType.HOBBY, "취미")
        asset = ChoiceItem(PreferenceMetaType.RELIGION, "종교")
        family_asset = ChoiceItem(PreferenceMetaType.DATE_STYLE, "데이트 스타일")
        car = ChoiceItem(PreferenceMetaType.MBTI, "MBTI")

    type = models.CharField("타입", choices=PreferenceMetaTypeChoices.choices, blank=False, null=False, db_index=True)
    value = models.CharField("마지막 값", blank=False, null=True, default=None)

    class Meta:
        db_table = "preference_meta_preset"
        verbose_name = "[preference_meta_preset] 기호 정보 선택지"
        verbose_name_plural = "[preference_meta_preset] 기호 정보 선택지"

    def __str__(self) -> str:
        return f"[id: {self.id}] [type: {self.type}] [value: {self.value}]"


class MemberPreferenceMetaORM(TimeStampedModel):
    member_id = models.PositiveIntegerField(db_index=True, null=False, blank=False)
    preference_meta = models.ForeignKey(
        PreferenceMetaPresetORM, on_delete=models.CASCADE, related_name="member_preference_meta", blank=False, null=True
    )

    class Meta:
        db_table = "member_preference_meta"
        verbose_name = "[member_preference_meta] 사용자 기호 정보"
        verbose_name_plural = "[member_preference_meta] 사용자 기호 정보"

    def __str__(self) -> str:
        return f"[id: {self.id}] [member_id: {self.member_id}] [value: {self.preference_meta}]"
