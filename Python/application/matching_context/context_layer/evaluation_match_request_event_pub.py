from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.context_layer.subscriber.evaluation_match_requset_event_sub import (
    EvaluationMatchRequestEventSubscriber,
)
from application.matching_context.domain_layer.value_object.ideal_member_evaluation_point_set import (
    IdealMemberEvaluationPointSet,
)


class EvaluationMatchRequestEventPublisher:
    @classmethod
    def publish_evaluation_match_request(
        cls,
        min_ideal_evaluation_point_set: IdealMemberEvaluationPointSet,
        max_ideal_evaluation_point_set: IdealMemberEvaluationPointSet,
        ideal_gender: Gender,
    ) -> list[MemberID]:
        return EvaluationMatchRequestEventSubscriber.subscribe_evaluation_match_request(
            min_evaluation_point_set=min_ideal_evaluation_point_set,
            max_evaluation_point_set=max_ideal_evaluation_point_set,
            ideal_gender=ideal_gender,
        )
