from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.entity.member_evaluation import (
    MemberEvaluation,
)
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.evaluation_context.infra_layer.repository.evaluation_repositories import (
    EvaluationCompoundRepository,
)


class MemberEvaluationFindService:

    repo: EvaluationCompoundRepository

    def __init__(self, repo: EvaluationCompoundRepository = EvaluationCompoundRepository()):
        self.repo = repo

    def find_by_member_id(self, member_id: MemberID) -> MemberEvaluation:
        return MemberEvaluation(member_id=member_id)

    def find_all_by_range(
        self, min_evaluation_point_set: EvaluationPointSet, max_evaluation_point_set: EvaluationPointSet, gender: Gender
    ) -> list[MemberID]:
        return self.repo.find_all_by(
            min_evaluation_point_set=min_evaluation_point_set,
            max_evaluation_point_set=max_evaluation_point_set,
            gender=gender,
        )
