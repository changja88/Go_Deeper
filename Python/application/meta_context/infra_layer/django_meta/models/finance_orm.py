from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.infra_layer.django_meta.models import CertificationORM


class FinanceMetaPresetORM(models.Model):
    class FinanceMetaTypeChoices(DjangoChoices):
        job = ChoiceItem(FinanceMetaType.JOB, "직업")
        income = ChoiceItem(FinanceMetaType.INCOME, "소득")
        company = ChoiceItem(FinanceMetaType.COMPANY, "회사")
        asset = ChoiceItem(FinanceMetaType.ASSET, "자산")
        family_asset = ChoiceItem(FinanceMetaType.FAMILY_ASSET, "집안 자산")
        car_brand = ChoiceItem(FinanceMetaType.CAR_BRAND, "차량 브랜드")
        car_price = ChoiceItem(FinanceMetaType.CAR_PRICE, "차량 가격")
        mother_job = ChoiceItem(FinanceMetaType.MOTHER_JOB, "모 직업")
        father_job = ChoiceItem(FinanceMetaType.FATHER_JOB, "부 직업")

    value = models.CharField("경제력 메타 값", null=False, blank=False)
    type = models.CharField("타입", choices=FinanceMetaTypeChoices.choices, blank=False, null=False, db_index=True)
    is_show = models.CharField("사용자 직접입력 값 승인여부", blank=False, null=False, default=True)
    tear = models.PositiveSmallIntegerField(null=False, default=0, help_text="평가 티어")

    class Meta:
        db_table = "finance_meta_preset"
        verbose_name = "[finance_meta_preset] 경제력 정보 선택지"
        verbose_name_plural = "[finance_meta_preset] 경제력 정보 선택지"

    def __str__(self) -> str:
        return f"[id: {self.id}] [value: {self.value}]"


class MemberFinanceMetaORM(CertificationORM):
    member_id = models.PositiveIntegerField(db_index=True, null=False, blank=False)
    finance_meta = models.ForeignKey(
        FinanceMetaPresetORM, on_delete=models.CASCADE, related_name="member_finance_meta", blank=False, null=True
    )

    class Meta:
        db_table = "member_finance_meta"
        verbose_name = "[member_finance_meta] 사용자 경제력 정보"
        verbose_name_plural = "[member_finance_meta] 사용자 경제력 계정"

    def __str__(self) -> str:
        return f"[id: {self.member_id}] [job: {self.finance_meta}]"
