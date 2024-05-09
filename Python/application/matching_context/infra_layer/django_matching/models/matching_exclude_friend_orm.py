from django.db import models
from model_utils.models import TimeStampedModel

from application.member_context.infra_layer.django.models import MemberORM


class MatchingExcludeFriendORM(TimeStampedModel):
    member = models.ForeignKey(
        MemberORM,
        on_delete=models.CASCADE,
        related_name="matching_exclude_friend",
        db_index=True,
        help_text="친구 주인",
    )

    phone_number = models.PositiveIntegerField(null=False, blank=False, help_text="지인 번호")
    name = models.CharField(null=False, blank=False, help_text="지인 이름")

    class Meta:
        db_table = "matching_exclude_friend"
        verbose_name = "[matching_exclude_friend] 멤버 추천 제외 친구 목록"
        verbose_name_plural = "[matching_exclude_friend] 멤버 추천 제외 친구 목록"

    def __str__(self) -> str:
        return f"[id: {self.id}] [member: {self.member}] [phone_number: {self.phone_number}]"
