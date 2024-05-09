from django.db import models
from django_extensions.db.models import TimeStampedModel

from application.member_context.infra_layer.django.models import MemberORM


class DateTestMetaQuestionPresetORM(models.Model):
    question = models.CharField("연애고사 질문", blank=False, null=False)
    type = models.CharField("연애고사 질문 타입", blank=False, null=False)
    order = models.PositiveIntegerField("질문 순서", blank=False, null=False)

    class Meta:
        db_table = "date_test_meta_question"
        verbose_name = "[date_test_meta_question] 연애 고사 질문지"
        verbose_name_plural = "[date_test_meta_question] 연애 고사 질문지"

    def __str__(self) -> str:
        return f"[id: {self.id}] [question: {self.question}]"


class DateTestMetaAnswerPresetORM(models.Model):
    answer = models.CharField("연애고사 답변", blank=False, null=False)
    question = models.ForeignKey(
        DateTestMetaQuestionPresetORM, related_name="answer", on_delete=models.CASCADE, null=False, blank=False
    )
    order = models.PositiveIntegerField("표기 순서", blank=False, null=False)

    class Meta:
        db_table = "date_test_meta_answer"
        verbose_name = "[date_test_meta_answer] 연애 고사 답변"
        verbose_name_plural = "[date_test_meta_answer] 연애 고사 답변"

    def __str__(self) -> str:
        return f"[id: {self.id}] [question: {self.question}] [answer: {self.answer}]"


class MemberDateTestMetaORM(TimeStampedModel):
    member = models.ForeignKey(MemberORM, on_delete=models.CASCADE, null=False, blank=False, db_index=True)
    question = models.ForeignKey(DateTestMetaQuestionPresetORM, on_delete=models.CASCADE, null=False, blank=False)
    answer = models.ForeignKey(DateTestMetaAnswerPresetORM, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        db_table = "member_date_test_meta"
        verbose_name = "[member_date_test_meta] 멤버 연애 고사 답변"
        verbose_name_plural = "[member_date_test_meta] 멤버 연애 고사 답변"
        constraints = [
            models.UniqueConstraint(fields=["member", "question", "answer"], name="member_date_test_result_unique"),
        ]

    def __str__(self) -> str:
        return f"[id: {self.id}] [question: {self.question}] [answer: {self.answer}]"
