from typing import Optional

from pydantic import BaseModel, PositiveInt

from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_physical_meta import (
    MemberPhysicalMeta,
)
from application.meta_context.domain_layer.meta_enum import PhysicalMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.lookup_physical_meta_repositories import (
    PhysicalMetaLookupCompoundRepository,
)


class MemberPhysicalMetaInput(BaseModel):
    member_id: MemberID
    meta_id: PositiveInt


class MemberPhysicalMetaService:
    repo: PhysicalMetaLookupCompoundRepository

    def __init__(self, repo: PhysicalMetaLookupCompoundRepository = PhysicalMetaLookupCompoundRepository()):
        self.repo = repo

    def find_by_member_id(self, member_id: MemberID) -> MemberPhysicalMeta:
        return MemberPhysicalMeta(member_id=member_id)

    def update_member_physical_meta(self, update_request: MemberPhysicalMetaInput) -> MemberPhysicalMeta:
        member_meta: MemberPhysicalMeta = MemberPhysicalMeta(member_id=update_request.member_id)
        base_physical_meta: Optional[Meta]
        if base_physical_meta := self.repo.find_by_id(meta_id=update_request.meta_id):
            member_meta.update_physical_meta(
                meta_id=update_request.meta_id, meta_type=PhysicalMetaType(base_physical_meta.type)
            )
        return member_meta
