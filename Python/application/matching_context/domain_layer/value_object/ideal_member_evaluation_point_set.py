from typing import NewType

from application.evaluation_context.domain_layer.value_object.evaluation_point_set import (
    EvaluationPointSet,
)

IdealMemberEvaluationPointSet = NewType("IdealMemberEvaluationPointSet", EvaluationPointSet)
