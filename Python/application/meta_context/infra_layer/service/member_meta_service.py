from pydantic import BaseModel, PositiveInt

from applications.common.enum import Gender
from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_physical_meta import (
    MemberPhysicalMeta,
)
from application.meta_context.infra_layer.repository.lookup_physical_meta_repositories import (
    PhysicalMetaLookupCompoundRepository,
)


class RegisterEvent(BaseModel):
    member_id: MemberID
    gender: str
    birth_year: PositiveInt


class MemberMetaService:
    repo: PhysicalMetaLookupCompoundRepository

    def __init__(self, repo: PhysicalMetaLookupCompoundRepository = PhysicalMetaLookupCompoundRepository()):
        self.repo = repo

    def register_birth_meta_from_register_event(self, register_event: RegisterEvent) -> MemberPhysicalMeta:
        return MemberPhysicalMeta.get_instance(
            member_id=register_event.member_id,
            gender=Gender(register_event.gender),
            birth_year=register_event.birth_year,
        )

    def find_by(self, member_id: MemberID) -> MemberPhysicalMeta:
        return MemberPhysicalMeta(member_id=member_id)
