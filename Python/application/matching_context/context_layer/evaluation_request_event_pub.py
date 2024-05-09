from applications.common.type import MemberID
from application.evaluation_context.context_layer.subscriber.evaluation_request_event_sub import (
    EvaluationRequestEventSubscriber,
)
from application.evaluation_context.domain_layer.entity.member_evaluation import (
    MemberEvaluation,
)


class EvaluationRequestEventPublisher:
    @classmethod
    def publish_evaluation_request(cls, member_id: MemberID) -> MemberEvaluation:
        return EvaluationRequestEventSubscriber.subscribe_evaluation_request(member_id=member_id)
