from datetime import datetime
from decimal import Decimal
from typing import Any

from pydantic import PositiveInt

from applications.common.enum import Gender
from applications.common.ninja.custom_entity_model import ValueObject


class AgeRangeWithTear(ValueObject):
    age_range: Any
    tear: Decimal


male_standard_list = [
    AgeRangeWithTear(age_range=range(0, 19), tear=Decimal("0")),
    AgeRangeWithTear(age_range=range(22, 25), tear=Decimal("2.86")),
    AgeRangeWithTear(age_range=range(25, 30), tear=Decimal("8.57")),
    AgeRangeWithTear(age_range=range(30, 34), tear=Decimal("10.0")),
    AgeRangeWithTear(age_range=range(34, 37), tear=Decimal("8.57")),
    AgeRangeWithTear(age_range=range(37, 40), tear=Decimal("7.14")),
    AgeRangeWithTear(age_range=range(40, 43), tear=Decimal("5.71")),
    AgeRangeWithTear(age_range=range(43, 46), tear=Decimal("4.29")),
    AgeRangeWithTear(age_range=range(46, 48), tear=Decimal("2.86")),
    AgeRangeWithTear(age_range=range(48, 50), tear=Decimal("1.43")),
    AgeRangeWithTear(age_range=range(50, 100), tear=Decimal("0")),
]
female_standard_list = [
    AgeRangeWithTear(age_range=range(0, 22), tear=Decimal("0")),
    AgeRangeWithTear(age_range=range(22, 24), tear=Decimal("2.86")),
    AgeRangeWithTear(age_range=range(24, 26), tear=Decimal("8.57")),
    AgeRangeWithTear(age_range=range(26, 30), tear=Decimal("10.0")),
    AgeRangeWithTear(age_range=range(30, 33), tear=Decimal("8.57")),
    AgeRangeWithTear(age_range=range(33, 35), tear=Decimal("7.14")),
    AgeRangeWithTear(age_range=range(35, 37), tear=Decimal("5.71")),
    AgeRangeWithTear(age_range=range(37, 40), tear=Decimal("4.29")),
    AgeRangeWithTear(age_range=range(40, 46), tear=Decimal("2.86")),
    AgeRangeWithTear(age_range=range(46, 50), tear=Decimal("1.43")),
    AgeRangeWithTear(age_range=range(50, 100), tear=Decimal("0")),
]


class BirthYearEvaluationStandard(ValueObject):
    male_standard_list: list[AgeRangeWithTear] = male_standard_list
    female_standard_list: list[AgeRangeWithTear] = female_standard_list

    def _parse_birth_year_to_age(self, birth_year: PositiveInt) -> PositiveInt:
        current_year = datetime.now().year
        return (current_year - birth_year) + 1

    def find_tear_by(self, gender: Gender, birth_year: PositiveInt) -> Decimal:
        age = self._parse_birth_year_to_age(birth_year=birth_year)
        if gender == Gender.MALE:
            standard_list = self.male_standard_list
        else:
            standard_list = self.male_standard_list

        for standard in standard_list:
            if age in standard.age_range:
                return standard.tear
        return Decimal("0")
