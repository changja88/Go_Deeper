from pydantic import PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject


class EvaluationSource(ValueObject):
    weight: PositiveInt
