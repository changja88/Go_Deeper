from typing import Self

from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import Entity
from applications.common.type import MemberID
from application.evaluation_context.domain_layer.value_object.evaluation_point import (
    EvaluationPoint,
)
from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)
from application.evaluation_context.infra_layer.repository.evaluation_repositories import (
    EvaluationCompoundRepository,
)


class MemberEvaluation(Entity):
    member_id: MemberID
    evaluation_point_set: EvaluationPointSet
    repo: SkipJsonSchema[EvaluationCompoundRepository] = Field(exclude=True)

    def __init__(
        self, member_id: MemberID, evaluation_point_set: EvaluationPointSet, repo: EvaluationCompoundRepository
    ):
        super().__init__(member_id=member_id, evaluation_point_set=evaluation_point_set, repo=repo)

    @classmethod
    def find_from_rds(cls, entity_id: PositiveInt) -> Self:
        repo: EvaluationCompoundRepository = EvaluationCompoundRepository()
        return cls(
            member_id=entity_id,
            evaluation_point_set=repo.find_by_member_id(member_id=entity_id),
            repo=repo,
        )

    def register_work_evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.work_point = self.repo.update_or_create_work_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self

    def register_asset_evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.asset_point = self.repo.update_or_create_asset_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self

    def register_background_evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.background_point = self.repo.update_or_create_background_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self

    def register_income_evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.income_point = self.repo.update_or_create_income_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self

    def register_birth_year_evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.birth_year_point = self.repo.update_or_create_birth_year_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self

    def calculate_edcuation_evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.education_point = self.repo.update_or_create_education_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self

    def register_appearance__evaluation_point(self, evaluation_point: EvaluationPoint) -> Self:
        self.evaluation_point_set.appearance_point = self.repo.update_or_create_appearance_evaluation_point(
            member_id=self.member_id, evaluation_point=evaluation_point
        )
        return self
