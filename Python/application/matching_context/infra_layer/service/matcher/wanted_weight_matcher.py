from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.entity.member_evaluation import (
    MemberEvaluation,
)
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.matching_context.context_layer.evaluation_request_event_pub import (
    EvaluationRequestEventPublisher,
)
from application.matching_context.context_layer.member_meta_request_event_pub import (
    MemberMetaRequestEventPublisher,
)
from application.matching_context.context_layer.wanted_info_request_event_pub import (
    WantedInfoRequestEventPublisher,
)
from application.matching_context.domain_layer.matching_enum import (
    IDEAL_EVALUATION_POINT_RANGE_PERCENTAGE,
)
from application.matching_context.domain_layer.value_object.ideal_member_evaluation_point_set import (
    IdealMemberEvaluationPointSet,
)
from application.matching_context.infra_layer.service.helper.ideal_member_evaluation_point_set_maker import (
    IdealMemberEvaluationPointSetMaker,
)
from application.matching_context.infra_layer.service.helper.ideal_member_finder import (
    IdealMemberFinder,
)
from application.meta_context.domain_layer.entity.member_physical_meta import (
    MemberPhysicalMeta,
)
from application.wanted_context.domain_layer.entity.member_wanted_info import (
    MemberWantedInfo,
)
from application.wanted_context.domain_layer.value_object.wanted_weight import (
    WantedWeight,
)
from application.wanted_context.domain_layer.wanted_enum import (
    AVAILABLE_WANTED_WEIGHT_POINT_TOTAL,
    WANTED_POINT_CUT_OFF_PERCENTAGE,
)


class WantedWeightMatcher:

    member_id: MemberID

    def __init__(self, member_id: MemberID) -> None:
        self.member_id = member_id

    def find_matched_member_list(self) -> list[MemberID]:
        ideal_members: list[MemberID] = IdealMemberFinder(
            ideal_evaluation_point_range_percentage=IDEAL_EVALUATION_POINT_RANGE_PERCENTAGE,
        ).find_ideal_members_by(
            ideal_evaluation_point_set=self._get_ideal_evaluation_point_set(),
            ideal_gender=self._get_ideal_member_gender(),
        )
        return ideal_members

    def _get_ideal_evaluation_point_set(self) -> IdealMemberEvaluationPointSet:
        ideal_evaluation_point_set: IdealMemberEvaluationPointSet = IdealMemberEvaluationPointSetMaker(
            cut_ff_percentage=WANTED_POINT_CUT_OFF_PERCENTAGE,
            wanted_weight_point_total=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default,
        ).make(
            member_wanted_weight=self._get_member_wanted_weight(),
            member_evaluation_point_set=self._get_member_evaluation_point_set(),
        )
        return ideal_evaluation_point_set

    def _get_ideal_member_gender(self) -> Gender:
        member_meta: MemberPhysicalMeta = MemberMetaRequestEventPublisher.publish_member_physical_meta_request_event(
            member_id=self.member_id
        )
        return Gender.FEMALE if member_meta.gender == Gender.MALE else Gender.MALE

    def _get_member_evaluation_point_set(self) -> EvaluationPointSet:
        target_member_evaluation_point: MemberEvaluation = EvaluationRequestEventPublisher.publish_evaluation_request(
            member_id=self.member_id
        )
        return target_member_evaluation_point.evaluation_point_set

    def _get_member_wanted_weight(self) -> WantedWeight:
        target_member_wanted_info: MemberWantedInfo = (
            WantedInfoRequestEventPublisher.publish_member_wanted_info_request_event(member_id=self.member_id)
        )
        return target_member_wanted_info.wanted_weight
