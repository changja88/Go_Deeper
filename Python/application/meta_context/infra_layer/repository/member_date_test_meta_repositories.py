from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import get_list_or_none
from applications.common.type import MemberID
from application.meta_context.domain_layer.value_object.meta.date_test import (
    Answer,
    ProblemResponse,
    Question,
)
from application.meta_context.infra_layer.django_meta.models import (
    MemberDateTestMetaORM,
)


class MemberDateTestMetaReadRepository:
    def find_by(self, member_id: MemberID) -> list[ProblemResponse]:
        member_date_test_orm_list: Optional[list[MemberDateTestMetaORM]] = get_list_or_none(
            MemberDateTestMetaORM, member_id=member_id
        )
        answers: list[ProblemResponse] = []
        if member_date_test_orm_list:
            for member_date_test_orm in member_date_test_orm_list:
                question: Question = Question(
                    id=member_date_test_orm.question.id,
                    type=member_date_test_orm.question.type,
                    question=member_date_test_orm.question.question,
                    order=member_date_test_orm.question.order,
                )
                answer: Answer = Answer(
                    id=member_date_test_orm.answer.id,
                    order=member_date_test_orm.answer.order,
                    answer=member_date_test_orm.answer.answer,
                )
                answers.append(ProblemResponse(question=question, answer=answer))
        return answers


class MemberDateTestMetaWriteRepository:
    def create_or_update(
        self, member_id: MemberID, question_id: PositiveInt, answer_id: PositiveInt
    ) -> ProblemResponse:
        member_date_test_orm: MemberDateTestMetaORM
        member_date_test_orm, _ = MemberDateTestMetaORM.objects.update_or_create(
            member_id=member_id,
            question_id=question_id,
            defaults={"member_id": member_id, "question_id": question_id, "answer_id": answer_id},
        )
        return ProblemResponse(
            question=Question(
                id=member_date_test_orm.question.id,
                type=member_date_test_orm.question.type,
                question=member_date_test_orm.question.question,
                order=member_date_test_orm.question.order,
            ),
            answer=Answer(
                id=member_date_test_orm.answer.id,
                order=member_date_test_orm.answer.order,
                answer=member_date_test_orm.answer.answer,
            ),
        )


class MemberDateTestMetaCompoundRepository(MemberDateTestMetaReadRepository, MemberDateTestMetaWriteRepository): ...
