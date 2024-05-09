from pydantic import Field, NonNegativeInt, PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject
from application.meta_context.domain_layer.meta_enum import MetaType
from application.meta_context.domain_layer.value_object.certification.meta_certification import (
    Certification,
)


class Meta(ValueObject):
    id: PositiveInt
    value: str
    type: MetaType


class CertifiableMeta(Meta):
    tear: NonNegativeInt = Field(exclude=True)
    certification: Certification
