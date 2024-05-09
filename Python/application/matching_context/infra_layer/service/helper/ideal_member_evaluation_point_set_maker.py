from decimal import Decimal

from pydantic import PositiveInt

from application.evaluation_context.domain_layer.value_object.evaluation_point import (
    EvaluationPoint,
)
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.matching_context.domain_layer.value_object.ideal_member_evaluation_point_set import (
    IdealMemberEvaluationPointSet,
)
from application.wanted_context.domain_layer.value_object.wanted_weight import (
    WantedWeight,
)


class IdealMemberEvaluationPointSetMaker:
    CUT_OFF_PERCENTAGE: PositiveInt
    WANTED_WEIGHT_POINT_TOTAL: PositiveInt

    def __init__(self, cut_ff_percentage: PositiveInt, wanted_weight_point_total: PositiveInt):
        self.CUT_OFF_PERCENTAGE = cut_ff_percentage
        self.WANTED_WEIGHT_POINT_TOTAL = wanted_weight_point_total

    def make(
        self, member_wanted_weight: WantedWeight, member_evaluation_point_set: EvaluationPointSet
    ) -> IdealMemberEvaluationPointSet:
        cut_offed_member_evaluation_point_set: EvaluationPointSet
        remain_evaluation_point: EvaluationPoint

        cut_offed_member_evaluation_point_set, remain_evaluation_point = self._cut_off_member_evaluation_point_set(
            evaluation_point_set=member_evaluation_point_set,
        )
        wanted_weight_applied_evaluation_point_set: EvaluationPointSet = self._apply_wanted_weight(
            cut_offed_evaluation_point_set=cut_offed_member_evaluation_point_set,
            remain_evaluation_point=remain_evaluation_point,
            wanted_weight=member_wanted_weight,
        )
        return IdealMemberEvaluationPointSet(wanted_weight_applied_evaluation_point_set)

    def _cut_off_member_evaluation_point_set(
        self, evaluation_point_set: EvaluationPointSet
    ) -> tuple[EvaluationPointSet, EvaluationPoint]:
        cut_offed_work_point = evaluation_point_set.work_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)
        cut_offed_income_point = evaluation_point_set.income_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)
        cut_offed_asset_point = evaluation_point_set.asset_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)
        cut_offed_background_point = evaluation_point_set.background_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)
        cut_offed_education_point = evaluation_point_set.education_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)
        cut_offed_appearance_point = evaluation_point_set.appearance_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)
        cut_offed_birth_year_point = evaluation_point_set.birth_year_point * Decimal(1 - self.CUT_OFF_PERCENTAGE / 100)

        remain_point: EvaluationPoint = (
            evaluation_point_set.work_point
            - cut_offed_work_point
            + evaluation_point_set.income_point
            - cut_offed_income_point
            + evaluation_point_set.asset_point
            - cut_offed_asset_point
            + evaluation_point_set.background_point
            - cut_offed_background_point
            + evaluation_point_set.education_point
            - cut_offed_education_point
            + evaluation_point_set.appearance_point
            - cut_offed_appearance_point
            + evaluation_point_set.birth_year_point
            - cut_offed_birth_year_point
        )

        return (
            EvaluationPointSet(
                work_point=cut_offed_work_point,
                income_point=cut_offed_income_point,
                asset_point=cut_offed_asset_point,
                background_point=cut_offed_background_point,
                education_point=cut_offed_education_point,
                appearance_point=cut_offed_appearance_point,
                birth_year_point=cut_offed_birth_year_point,
            ),
            remain_point,
        )

    def _apply_wanted_weight(
        self,
        cut_offed_evaluation_point_set: EvaluationPointSet,
        wanted_weight: WantedWeight,
        remain_evaluation_point: EvaluationPoint,
    ) -> EvaluationPointSet:
        evaluation_point_per_wanted_weight: EvaluationPoint = remain_evaluation_point / Decimal(
            self.WANTED_WEIGHT_POINT_TOTAL
        )

        return EvaluationPointSet(
            work_point=cut_offed_evaluation_point_set.work_point
            + (evaluation_point_per_wanted_weight * wanted_weight.work_weight),
            income_point=cut_offed_evaluation_point_set.income_point
            + (evaluation_point_per_wanted_weight * wanted_weight.income_weight),
            asset_point=cut_offed_evaluation_point_set.asset_point
            + (evaluation_point_per_wanted_weight * wanted_weight.asset_weight),
            background_point=cut_offed_evaluation_point_set.background_point
            + (evaluation_point_per_wanted_weight * wanted_weight.background_weight),
            education_point=cut_offed_evaluation_point_set.education_point
            + (evaluation_point_per_wanted_weight * wanted_weight.education_weight),
            appearance_point=cut_offed_evaluation_point_set.appearance_point
            + (evaluation_point_per_wanted_weight * wanted_weight.appearance_weight),
            birth_year_point=cut_offed_evaluation_point_set.birth_year_point
            + (evaluation_point_per_wanted_weight * wanted_weight.birth_year_weight),
        )
