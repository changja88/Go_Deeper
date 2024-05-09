from decimal import Decimal
from typing import Any, Self

from pydantic import Field, NonNegativeFloat, field_validator

from applications.common.ninja.custom_entity_model import ValueObject


class EvaluationPoint(ValueObject):
    point: Decimal = Field(le=100)

    def __init__(self, point: NonNegativeFloat):
        super().__init__(point=Decimal(str(point)))

    @field_validator("point")
    @classmethod
    def double(cls, value: Decimal) -> Decimal:
        return round(value, 5)

    def __mul__(self, other: Any) -> Self:
        return EvaluationPoint(self.point * Decimal(str(other)))

    def __truediv__(self, other: Any) -> Self:
        return EvaluationPoint(self.point / Decimal(str(other)))

    def __add__(self, other: Self) -> Self:
        result = self.point + other.point
        return EvaluationPoint(point=result)

    def __sub__(self, other: Self) -> Self:
        result = self.point - other.point
        return EvaluationPoint(point=result)

    def __lt__(self, other: Self) -> bool:
        return self.point < other.point

    def __le__(self, other: Self) -> bool:
        return self.point <= other.point

    def __gt__(self, other: Self) -> bool:
        return self.point > other.point

    def __ge__(self, other: Self) -> bool:
        return self.point >= other.point

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, EvaluationPoint):
            return False
        return self.point == other.point

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, EvaluationPoint):
            return False
        return self.point != other.point
