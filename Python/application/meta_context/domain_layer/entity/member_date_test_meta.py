from typing import Optional, Self

from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.value_object.meta.date_test import (
    Answer,
    ProblemResponse,
)
from application.meta_context.infra_layer.repository.member_date_test_meta_repositories import (
    MemberDateTestMetaCompoundRepository,
)


class MemberDateTestMeta(ValueObject):
    member_id: MemberID
    responses: list[ProblemResponse]
    repo: SkipJsonSchema[MemberDateTestMetaCompoundRepository] = Field(exclude=True)

    def __init__(
        self, member_id: MemberID, repo: MemberDateTestMetaCompoundRepository = MemberDateTestMetaCompoundRepository()
    ):
        super().__init__(member_id=member_id, responses=repo.find_by(member_id=member_id), repo=repo)

    def register_answer(self, question_id: PositiveInt, answer_id: PositiveInt) -> Self:
        self._delete_previous_answer(question_id=question_id)
        self.responses.append(
            self.repo.create_or_update(member_id=self.member_id, question_id=question_id, answer_id=answer_id)
        )
        return self

    def _delete_previous_answer(self, question_id: PositiveInt) -> None:
        self.responses = [response for response in self.responses if response.question.id != question_id]

    def get_answer_of(self, question_id: PositiveInt) -> Optional[Answer]:
        for problem_response in self.responses:
            if problem_response.question.id == question_id:
                return problem_response.answer
        return None
