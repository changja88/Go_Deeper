from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.evaluation_context.infra_layer.service.member_evaluation_find_service import (
    MemberEvaluationFindService,
)


class EvaluationMatchRequestEventSubscriber:
    @classmethod
    def subscribe_evaluation_match_request(
        cls,
        min_evaluation_point_set: EvaluationPointSet,
        max_evaluation_point_set: EvaluationPointSet,
        ideal_gender: Gender,
    ) -> list[MemberID]:
        return MemberEvaluationFindService().find_all_by_range(
            min_evaluation_point_set=min_evaluation_point_set,
            max_evaluation_point_set=max_evaluation_point_set,
            gender=ideal_gender,
        )
