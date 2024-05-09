from typing import Optional, Self

from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.value_object.meta.meta import CertifiableMeta
from application.meta_context.infra_layer.repository.member_education_repositories import (
    MemberEducationMetaCompoundRepository,
)


class MemberEducationMeta(ValueObject):
    member_id: MemberID
    university: Optional[CertifiableMeta]
    repo: SkipJsonSchema[MemberEducationMetaCompoundRepository] = Field(exclude=True)

    def __init__(
        self,
        member_id: MemberID,
        repo: MemberEducationMetaCompoundRepository = MemberEducationMetaCompoundRepository(),
    ):
        super().__init__(member_id=member_id, university=repo.find_by(member_id=member_id), repo=repo)

    def register_university(self, meta_id: PositiveInt) -> Self:
        new_education_meta: CertifiableMeta = self.repo.update_or_create(meta_id=meta_id, member_id=self.member_id)
        self.university = new_education_meta
        return self
