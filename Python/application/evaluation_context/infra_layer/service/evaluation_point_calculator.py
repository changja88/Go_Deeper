from typing import Optional

from pydantic import NonNegativeInt, PositiveInt

from applications.common.enum import Gender
from application.evaluation_context.domain_layer.value_object.birth_year_evaluation_standard import (
    BirthYearEvaluationStandard,
)
from application.evaluation_context.domain_layer.value_object.evaluation_point import (
    EvaluationPoint,
)
from application.evaluation_context.domain_layer.value_object.evaluation_source_set import (
    EvaluationSourceSet,
)


class EvaluationPointCalculator:
    meta_max_tear: PositiveInt
    evaluation_source_set: EvaluationSourceSet

    def __init__(self, meta_max_tear: PositiveInt, evaluation_weight_standard: EvaluationSourceSet) -> None:
        self.evaluation_source_set = evaluation_weight_standard
        self.meta_max_tear = meta_max_tear

    def _calculate(self, tear: Optional[NonNegativeInt], evaluation_ratio: PositiveInt) -> EvaluationPoint:
        if not tear or tear == 0:
            return EvaluationPoint(0)
        else:
            return EvaluationPoint(evaluation_ratio * (tear / self.meta_max_tear))

    def calculate_work_evalualtion_point(
        self, company_meta_tear: Optional[NonNegativeInt], job_meta_tear: Optional[NonNegativeInt]
    ) -> EvaluationPoint:
        company_meta_point = self._calculate(
            tear=company_meta_tear, evaluation_ratio=self.evaluation_source_set.company_source.weight
        )
        job_meta_point = self._calculate(
            tear=job_meta_tear, evaluation_ratio=self.evaluation_source_set.job_source.weight
        )
        return company_meta_point + job_meta_point

    def calculate_income_evaluation_point(self, tear: Optional[NonNegativeInt]) -> EvaluationPoint:
        return self._calculate(tear=tear, evaluation_ratio=self.evaluation_source_set.income_source.weight)

    def calculate_education_meta(self, tear: Optional[NonNegativeInt]) -> EvaluationPoint:
        return self._calculate(tear=tear, evaluation_ratio=self.evaluation_source_set.education_source.weight)

    def calculate_birth_year_evaluation_point(self, gender: Gender, birth_year: PositiveInt) -> EvaluationPoint:
        birth_year_tear = BirthYearEvaluationStandard().find_tear_by(gender=gender, birth_year=birth_year)
        return self._calculate(
            tear=birth_year_tear, evaluation_ratio=self.evaluation_source_set.birth_year_source.weight
        )

    def calculate_background_evaluation_point(
        self,
        family_asset_tear: Optional[NonNegativeInt],
        father_job_meta_tear: Optional[NonNegativeInt],
        mother_job_meta_tear: Optional[NonNegativeInt],
    ) -> EvaluationPoint:
        """
        - 최대 리턴값은 total_asset_ratio(만점)을 넘을 수 없음
            - 집안 자산만으로 만점을 받을 수 있는데 추가로 부모직업 까지 반영해주면 만점을 넘을수 있어서 생긴 스펙
        - 집안 자산으로 만점을 찍지 못한경우 부모 직업을 반영해줌
        """
        if not family_asset_tear and not father_job_meta_tear and not mother_job_meta_tear:
            return EvaluationPoint(0)
        max_background_evaluation_point: EvaluationPoint = EvaluationPoint(
            self.evaluation_source_set.family_asset_source.weight
        )
        background_evaluation_point: EvaluationPoint = self._calculate(
            tear=family_asset_tear, evaluation_ratio=self.evaluation_source_set.family_asset_source.weight
        )
        father_job_evaluation_point: EvaluationPoint = self._calculate(
            tear=father_job_meta_tear, evaluation_ratio=self.evaluation_source_set.father_job_source.weight
        )
        mother_job_evaluation_point: EvaluationPoint = self._calculate(
            tear=mother_job_meta_tear, evaluation_ratio=self.evaluation_source_set.mother_job_source.weight
        )

        if background_evaluation_point == max_background_evaluation_point:
            return max_background_evaluation_point
        elif background_evaluation_point + father_job_evaluation_point >= max_background_evaluation_point:
            return max_background_evaluation_point
        elif background_evaluation_point + mother_job_evaluation_point >= max_background_evaluation_point:
            return max_background_evaluation_point
        elif (
            background_evaluation_point + father_job_evaluation_point + mother_job_evaluation_point
            > max_background_evaluation_point
        ):
            return max_background_evaluation_point
        else:
            return background_evaluation_point + father_job_evaluation_point + mother_job_evaluation_point

    def calculate_asset_evaluation_point(
        self, asset_tear: Optional[NonNegativeInt], car_price_tear: Optional[NonNegativeInt]
    ) -> EvaluationPoint:
        """
        - 최대 리턴값은 total_asset_ratio(만점)을 넘을 수 없음
            - 자산만으로 만점을 받을 수 있는데 추가로 차량 까지 반영해주면 만점을 넘을수 있어서 생긴 스펙
        - 자산으로 만점을 찍지 못한경우 차량 티어를 반영해줌
        """
        if not car_price_tear and not asset_tear:
            return EvaluationPoint(0)

        max_evaluation_point: EvaluationPoint = EvaluationPoint(self.evaluation_source_set.asset_source.weight)
        asset_evaluation_point: EvaluationPoint = self._calculate(
            tear=asset_tear, evaluation_ratio=self.evaluation_source_set.asset_source.weight
        )
        car_evaluation_point: EvaluationPoint = self._calculate(
            tear=car_price_tear, evaluation_ratio=self.evaluation_source_set.car_price_source_.weight
        )

        if asset_evaluation_point == max_evaluation_point:
            return max_evaluation_point
        elif asset_evaluation_point + car_evaluation_point > max_evaluation_point:
            return max_evaluation_point
        else:
            return asset_evaluation_point + car_evaluation_point
