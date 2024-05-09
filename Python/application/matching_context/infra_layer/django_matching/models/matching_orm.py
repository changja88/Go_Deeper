from django.db import models
from djchoices import ChoiceItem, DjangoChoices
from model_utils.models import TimeStampedModel

from application.matching_context.domain_layer.matching_enum import MatchingStatus
from application.member_context.infra_layer.django.models import MemberORM


class MatchingHistoryORM(TimeStampedModel):
    class MatchingStatusChoices(DjangoChoices):
        pending = ChoiceItem(MatchingStatus.PENDING, "대기중")
        approved = ChoiceItem(MatchingStatus.APPROVED, "수락")
        rejected = ChoiceItem(MatchingStatus.REJECTED, "거절")

    from_member = models.ForeignKey(
        MemberORM, on_delete=models.CASCADE, related_name="from_matching_history", db_index=True
    )
    to_member = models.ForeignKey(
        MemberORM, on_delete=models.CASCADE, related_name="to_matching_history", db_index=True
    )
    due_date = models.DateTimeField("추천 만기일", null=False, blank=False)
    reject_reason = models.TextField("거절 사유", null=True, blank=False)
    status = models.CharField(
        "매칭 응답 상태", choices=MatchingStatusChoices, blank=False, null=False, default=MatchingStatusChoices.pending
    )
    status2 = models.CharField(
        "매칭 응답 상태", choices=MatchingStatusChoices, blank=False, null=False, default=MatchingStatusChoices.pending
    )

    class Meta:
        db_table = "matching_history"
        verbose_name = "[matching_history] 멤버 매칭 기록"
        verbose_name_plural = "[matching_history] 멤버 매칭 기록"
        index_together = ("from_member", "to_member")

    def __str__(self) -> str:
        return f"[id: {self.id}] [from_member: {self.from_member.name}] [to_member: {self.to_member.name}]"
