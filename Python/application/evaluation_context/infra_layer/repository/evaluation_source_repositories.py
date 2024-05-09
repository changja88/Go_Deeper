from typing import Optional

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.enum import Gender
from application.evaluation_context.domain_layer.evaluation_enum import (
    EvaluationSourceType,
)
from application.evaluation_context.domain_layer.value_object.evaluation_source import (
    EvaluationSource,
)
from application.evaluation_context.infra_layer.django_evaluation.models import (
    EvaluationSourceORM,
)


class EvaluationSourceReadRepository:

    def find_evaluation_source_by(self, standard_type: EvaluationSourceType, gender: Gender) -> EvaluationSource:
        standard_orm: Optional[EvaluationSourceORM] = get_obj_or_none(
            EvaluationSourceORM, type=standard_type, gender=gender
        )
        if standard_orm:
            return EvaluationSource(weight=standard_orm.weight)
        return EvaluationSource(weight=0)


class EvaluationSourceWriteRepository:
    pass


class EvaluationSourceCompoundRepository(EvaluationSourceReadRepository, EvaluationSourceWriteRepository):
    pass
