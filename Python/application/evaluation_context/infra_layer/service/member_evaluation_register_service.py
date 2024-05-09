from functools import cached_property
from typing import Optional

from pydantic import NonNegativeInt, PositiveInt

from applications.common.enum import Gender
from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.entity.member_evaluation import (
    MemberEvaluation,
)
from application.evaluation_context.domain_layer.value_object.evaluation_source_set import (
    EvaluationSourceSet,
)
from application.evaluation_context.infra_layer.service.evaluation_point_calculator import (
    EvaluationPointCalculator,
)


class WorkMetaTearDataSet(ValueObject):
    job_meta_tear: Optional[NonNegativeInt]
    company_meta_tear: Optional[NonNegativeInt]


class AssetMetaTearDataSet(ValueObject):
    asset_meta_tear: Optional[NonNegativeInt]
    car_price_meta_tear: Optional[NonNegativeInt]


class BackgroundMetaTearDataSet(ValueObject):
    family_asset_meta_tear: Optional[NonNegativeInt]
    father_job_meta_tear: Optional[NonNegativeInt]
    mother_job_meta_tear: Optional[NonNegativeInt]


class MemberEvaluationRegisterService:
    META_MAX_TEAR: PositiveInt = 10

    def __init__(self, gender: Gender, member_id: MemberID):
        self.gender = gender
        self.member_id: MemberID = member_id

    @cached_property
    def evaluation_point_calculator(self) -> EvaluationPointCalculator:
        return EvaluationPointCalculator(
            meta_max_tear=self.META_MAX_TEAR,
            evaluation_weight_standard=EvaluationSourceSet(self.gender),
        )

    def register_work_evaluation_point(self, work_meta_tear_set: WorkMetaTearDataSet) -> MemberEvaluation:
        member_evaluation: MemberEvaluation = MemberEvaluation.find_from_rds(entity_id=self.member_id)
        work_evaluation_point = self.evaluation_point_calculator.calculate_work_evalualtion_point(
            company_meta_tear=work_meta_tear_set.company_meta_tear, job_meta_tear=work_meta_tear_set.job_meta_tear
        )
        member_evaluation.register_work_evaluation_point(evaluation_point=work_evaluation_point)
        return member_evaluation

    def register_income_evaluation_point(self, income_meta_tear: NonNegativeInt) -> MemberEvaluation:
        member_evaluation: MemberEvaluation = MemberEvaluation.find_from_rds(entity_id=self.member_id)
        work_evaluation_point = self.evaluation_point_calculator.calculate_income_evaluation_point(
            tear=income_meta_tear
        )
        member_evaluation.register_income_evaluation_point(evaluation_point=work_evaluation_point)
        return member_evaluation

    def register_asset_evaluation_point(self, asset_meta_tear_set: AssetMetaTearDataSet) -> MemberEvaluation:
        member_evaluation: MemberEvaluation = MemberEvaluation.find_from_rds(entity_id=self.member_id)
        asset_evaluation_point = self.evaluation_point_calculator.calculate_asset_evaluation_point(
            asset_tear=asset_meta_tear_set.asset_meta_tear, car_price_tear=asset_meta_tear_set.car_price_meta_tear
        )
        member_evaluation.register_asset_evaluation_point(evaluation_point=asset_evaluation_point)
        return member_evaluation

    def register_background_evaluation_point(
        self, background_meta_tear_set: BackgroundMetaTearDataSet
    ) -> MemberEvaluation:
        member_evaluation: MemberEvaluation = MemberEvaluation.find_from_rds(entity_id=self.member_id)
        background_evaluation_point = self.evaluation_point_calculator.calculate_background_evaluation_point(
            family_asset_tear=background_meta_tear_set.family_asset_meta_tear,
            father_job_meta_tear=background_meta_tear_set.father_job_meta_tear,
            mother_job_meta_tear=background_meta_tear_set.mother_job_meta_tear,
        )
        member_evaluation.register_background_evaluation_point(background_evaluation_point)
        return member_evaluation

    def register_education_meta_tear(self, education_meta_tear: NonNegativeInt) -> MemberEvaluation:
        member_evaluation: MemberEvaluation = MemberEvaluation.find_from_rds(entity_id=self.member_id)
        member_evaluation.calculate_edcuation_evaluation_point(
            evaluation_point=self.evaluation_point_calculator.calculate_education_meta(tear=education_meta_tear)
        )
        return member_evaluation

    def register_birth_year_evaluation_point(self, birth_year: PositiveInt) -> MemberEvaluation:
        member_evaluation: MemberEvaluation = MemberEvaluation.find_from_rds(entity_id=self.member_id)
        member_evaluation.register_birth_year_evaluation_point(
            evaluation_point=self.evaluation_point_calculator.calculate_birth_year_evaluation_point(
                gender=self.gender, birth_year=birth_year
            )
        )
        return member_evaluation

    def register_appearance_meta_tear(self, appearance_meta_tear: NonNegativeInt) -> None:
        # TODO: 등록된 멤버 사진 점수 매기는 관리자 페이지 만들 때 연동해야함
        pass
