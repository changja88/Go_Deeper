from applications.common.type import MemberID
from application.evaluation_context.domain_layer.entity.member_evaluation import (
    MemberEvaluation,
)
from application.evaluation_context.infra_layer.service.member_evaluation_find_service import (
    MemberEvaluationFindService,
)


class EvaluationRequestEventSubscriber:
    @classmethod
    def subscribe_evaluation_request(cls, member_id: MemberID) -> MemberEvaluation:
        return MemberEvaluationFindService().find_by_member_id(member_id=member_id)
