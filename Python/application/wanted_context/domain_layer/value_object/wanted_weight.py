from pydantic import Field, NonNegativeInt, computed_field

from applications.common.ninja.custom_entity_model import ValueObject
from application.wanted_context.domain_layer.wanted_enum import (
    AVAILABLE_WANTED_WEIGHT_POINT_TOTAL,
)


class WantedWeight(ValueObject):
    income_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)
    work_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)
    asset_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)
    background_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)
    education_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)
    appearance_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)
    birth_year_weight: NonNegativeInt = Field(default=0, le=AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default)

    @computed_field(repr=True)  # type: ignore[misc]
    @property
    def remain_point(self) -> NonNegativeInt:
        return AVAILABLE_WANTED_WEIGHT_POINT_TOTAL.default - (
            self.income_weight
            + self.work_weight
            + self.asset_weight
            + self.background_weight
            + self.education_weight
            + self.appearance_weight
            + self.birth_year_weight
        )

    def set_appearance_weight(self, appearance_weight: NonNegativeInt) -> None:
        self.appearance_weight = appearance_weight

    def set_birth_year_weight(self, age_weight: NonNegativeInt) -> None:
        self.birth_year_weight = age_weight

    def set_job_weight(self, job_weight: NonNegativeInt) -> None:
        self.work_weight = job_weight

    def set_income_weight(self, income_weight: NonNegativeInt) -> None:
        self.income_weight = income_weight

    def set_asset_weight(self, asset_weight: NonNegativeInt) -> None:
        self.asset_weight = asset_weight

    def set_education_weight(self, education_weight: NonNegativeInt) -> None:
        self.education_weight = education_weight

    def set_background_weight(self, background_weight: NonNegativeInt) -> None:
        self.background_weight = background_weight
