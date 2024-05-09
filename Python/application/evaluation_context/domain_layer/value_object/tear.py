from pydantic import Field, NonNegativeInt

from applications.common.ninja.custom_entity_model import ValueObject


class Tear(ValueObject):
    tear: NonNegativeInt = Field(le=10)
