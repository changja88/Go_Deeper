from applications.common.ninja.custom_entity_model import ValueObject
from application.evaluation_context.domain_layer.value_object.evaluation_point import (
    EvaluationPoint,
)


class EvaluationPointSet(ValueObject):
    work_point: EvaluationPoint
    income_point: EvaluationPoint
    asset_point: EvaluationPoint
    background_point: EvaluationPoint
    education_point: EvaluationPoint
    appearance_point: EvaluationPoint
    birth_year_point: EvaluationPoint
