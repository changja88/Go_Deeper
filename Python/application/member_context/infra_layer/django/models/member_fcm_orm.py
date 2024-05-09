from django.db import models
from django_extensions.db.models import TimeStampedModel


class MemberFCMORM(TimeStampedModel):
    member = models.ForeignKey("MemberORM", on_delete=models.CASCADE, db_index=True)
    fcm_token = models.CharField(blank=False, null=False, unique=True)
    device = models.CharField(
        blank=False,
        null=False,
    )

    class Meta:
        db_table = "member_fcm"
        verbose_name = "[member_fcm] 멤버 fcm 정보"
        verbose_name_plural = "[member_fcm] fcm 정보"
        constraints = [
            models.UniqueConstraint(fields=["member", "fcm_token"], name="member_fcm_unique"),
        ]

    def __str__(self) -> str:
        return f"[id: {self.id}] [member: {self.member.name}] [fcm_key: {self.fcm_token}]"
