from pydantic import PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_date_test_meta import (
    MemberDateTestMeta,
)
from application.meta_context.infra_layer.repository.member_date_test_meta_repositories import (
    MemberDateTestMetaCompoundRepository,
)


class MemberDateTestResponse(ValueObject):
    question_id: PositiveInt
    answer_id: PositiveInt


class MemberDateTestMetaService:
    repo: MemberDateTestMetaCompoundRepository

    def __init__(self, repo: MemberDateTestMetaCompoundRepository = MemberDateTestMetaCompoundRepository()):
        self.repo = repo

    def find_by(self, member_id: PositiveInt) -> MemberDateTestMeta:
        return MemberDateTestMeta(member_id=member_id)

    def register_member_date_test_response(
        self, member_id: MemberID, response: MemberDateTestResponse
    ) -> MemberDateTestMeta:
        member_date_test: MemberDateTestMeta = MemberDateTestMeta(member_id=member_id).register_answer(
            question_id=response.question_id, answer_id=response.answer_id
        )

        return member_date_test
