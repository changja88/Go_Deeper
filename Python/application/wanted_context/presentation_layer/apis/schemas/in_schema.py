from typing import Optional

from ninja import Schema
from pydantic import Field, PositiveInt

from application.meta_context.domain_layer.meta_enum import PreferenceMetaType


class MemberWantedWeightSchemaIn(Schema):
    appearance_weight: Optional[PositiveInt] = Field(default=None)
    birth_year_weight: Optional[PositiveInt] = Field(default=None)
    work_weight: Optional[PositiveInt] = Field(default=None)
    income_weight: Optional[PositiveInt] = Field(default=None)
    asset_weight: Optional[PositiveInt] = Field(default=None)
    education_weight: Optional[PositiveInt] = Field(default=None)
    background_weight: Optional[PositiveInt] = Field(default=None)


class MemberWantedPreferenceSchemaIn(Schema):
    meta_ids: list[PositiveInt]
    preference_type: PreferenceMetaType
