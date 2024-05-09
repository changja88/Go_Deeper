from collections import defaultdict

from django.db.models import QuerySet

from application.meta_context.domain_layer.value_object.meta.date_test import (
    Answer,
    DateTest,
    Problem,
    Question,
)
from application.meta_context.infra_layer.django_meta.models import (
    DateTestMetaAnswerPresetORM,
    DateTestMetaQuestionPresetORM,
)


class DateTestMetaLookupReadRepository:
    def find_all(self) -> DateTest:
        date_test_question_answer_set_orm_list: QuerySet = DateTestMetaAnswerPresetORM.objects.select_related(
            "question"
        ).all()
        grouped_date_test_question_answer_orm_list = self.group_date_test_set_orm(
            date_test_question_answer_queryset=date_test_question_answer_set_orm_list
        )
        date_test_unit_list: list[Problem] = self.make_date_test_unit_list(
            grouped_date_test_dict=grouped_date_test_question_answer_orm_list
        )
        result = DateTest(problems=date_test_unit_list)
        return result

    def make_date_test_unit_list(
        self, grouped_date_test_dict: dict[DateTestMetaQuestionPresetORM, list[DateTestMetaAnswerPresetORM]]
    ) -> list[Problem]:
        date_test_unit_list: list[Problem] = []
        for question_orm, answer_orm_list in grouped_date_test_dict.items():
            date_test_question: Question = Question(
                id=question_orm.id, type=question_orm.type, question=question_orm.question, order=question_orm.order
            )
            date_test_answer_list: list[Answer] = []
            for answer_orm in answer_orm_list:
                date_test_answer: Answer = Answer(id=answer_orm.id, order=answer_orm.order, answer=answer_orm.answer)
                date_test_answer_list.append(date_test_answer)
            date_test_unit_list.append(Problem(question=date_test_question, answers=date_test_answer_list))
        return date_test_unit_list

    def group_date_test_set_orm(
        self, date_test_question_answer_queryset: QuerySet
    ) -> dict[DateTestMetaQuestionPresetORM, list[DateTestMetaAnswerPresetORM]]:
        date_test_set_dict: dict[DateTestMetaQuestionPresetORM, list[DateTestMetaAnswerPresetORM]] = defaultdict(list)
        for date_test_question_answer in date_test_question_answer_queryset:
            date_test_set_dict[date_test_question_answer.question].append(date_test_question_answer)
        return date_test_set_dict


class DateTestMetaLookupWriteRepository:
    pass


class DateTestMetaLookupCompoundRepository(DateTestMetaLookupReadRepository, DateTestMetaLookupWriteRepository):
    pass
