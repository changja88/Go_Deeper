from pydantic import PositiveInt

from applications.common.enum import Gender
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.matching_context.context_layer.evaluation_match_request_event_pub import (
    EvaluationMatchRequestEventPublisher,
)
from application.matching_context.domain_layer.value_object.ideal_member_evaluation_point_set import (
    IdealMemberEvaluationPointSet,
)


class IdealMemberFinder:
    valid_range_percentage: PositiveInt

    def __init__(self, ideal_evaluation_point_range_percentage: PositiveInt):
        self.valid_range_percentage = ideal_evaluation_point_range_percentage

    def find_ideal_members_by(
        self, ideal_evaluation_point_set: IdealMemberEvaluationPointSet, ideal_gender: Gender
    ) -> list[MemberID]:
        min_evaluation_point_set, max_evaluation_point_set = self._calculate_min_and_max_evaluation_point_set(
            evaluation_point_set=ideal_evaluation_point_set
        )
        return EvaluationMatchRequestEventPublisher.publish_evaluation_match_request(
            min_ideal_evaluation_point_set=min_evaluation_point_set,
            max_ideal_evaluation_point_set=max_evaluation_point_set,
            ideal_gender=ideal_gender,
        )

    def _calculate_min_and_max_evaluation_point_set(
        self, evaluation_point_set: IdealMemberEvaluationPointSet
    ) -> tuple[IdealMemberEvaluationPointSet, IdealMemberEvaluationPointSet]:

        min_valid_percentage = 100 - self.valid_range_percentage
        max_valid_percentage = 100 + self.valid_range_percentage
        return (
            IdealMemberEvaluationPointSet(
                EvaluationPointSet(
                    work_point=evaluation_point_set.work_point * (min_valid_percentage / 100),
                    income_point=evaluation_point_set.income_point * (min_valid_percentage / 100),
                    asset_point=evaluation_point_set.asset_point * (min_valid_percentage / 100),
                    background_point=evaluation_point_set.background_point * (min_valid_percentage / 100),
                    education_point=evaluation_point_set.education_point * (min_valid_percentage / 100),
                    appearance_point=evaluation_point_set.appearance_point * (min_valid_percentage / 100),
                    birth_year_point=evaluation_point_set.birth_year_point * (min_valid_percentage / 100),
                )
            ),
            IdealMemberEvaluationPointSet(
                EvaluationPointSet(
                    work_point=evaluation_point_set.work_point * (max_valid_percentage / 100),
                    income_point=evaluation_point_set.income_point * (max_valid_percentage / 100),
                    asset_point=evaluation_point_set.asset_point * (max_valid_percentage / 100),
                    background_point=evaluation_point_set.background_point * (max_valid_percentage / 100),
                    education_point=evaluation_point_set.education_point * (max_valid_percentage / 100),
                    appearance_point=evaluation_point_set.appearance_point * (max_valid_percentage / 100),
                    birth_year_point=evaluation_point_set.birth_year_point * (max_valid_percentage / 100),
                )
            ),
        )
