from typing import Optional

from django.utils.functional import cached_property
from pydantic import PositiveInt

from application.matching_context.context_layer.member_date_test_request_event_pub import (
    DateTestMetaRequestEventPublisher,
)
from application.meta_context.domain_layer.entity.member_date_test_meta import (
    MemberDateTestMeta,
)
from application.meta_context.domain_layer.value_object.meta.date_test import (
    Answer,
    DateTest,
    Problem,
)


class DateTestSimilarityCalculator:

    @cached_property
    def date_test(self) -> DateTest:
        return DateTestMetaRequestEventPublisher.publish_date_test_request_event()

    def calculate_similarity(
        self, a_member_date_test: MemberDateTestMeta, b_member_date_test: MemberDateTestMeta
    ) -> PositiveInt:
        similarity_percentage_list: list[PositiveInt] = self._calcualte_similarity_percentage_per_problem(
            a_member_date_test=a_member_date_test,
            b_member_date_test=b_member_date_test,
        )
        return self._calculate_average_of_similarity_percentage(similarity_percentage_list=similarity_percentage_list)

    def _calculate_average_of_similarity_percentage(self, similarity_percentage_list: list[PositiveInt]) -> PositiveInt:
        mean = sum(similarity_percentage_list) / len(similarity_percentage_list)
        return round(mean)

    def _calcualte_similarity_percentage_per_problem(
        self, a_member_date_test: MemberDateTestMeta, b_member_date_test: MemberDateTestMeta
    ) -> list[PositiveInt]:
        # 문제별 일치율 퍼센테이지
        result: list[PositiveInt] = list()
        problem: Problem
        for problem in self.date_test.problems:
            possible_answer_count: PositiveInt = problem.get_answer_count_of()
            a_answer: Optional[Answer] = a_member_date_test.get_answer_of(problem.question.id)
            b_answer: Optional[Answer] = b_member_date_test.get_answer_of(problem.question.id)
            if not a_answer or not b_answer:
                result.append(0)
            elif a_answer.order == b_answer.order:
                result.append(100)
            else:
                result.append(
                    int((1 - round(abs(a_answer.order - b_answer.order) / (possible_answer_count - 1), 2)) * 100)
                )
        return result
