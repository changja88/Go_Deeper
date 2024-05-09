from typing import Optional, Self

from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.enum import Gender
from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import PhysicalMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.member_birth_meta_repositories import (
    MemberBirthMetaCompoundRepository,
)
from application.meta_context.infra_layer.repository.member_physical_meta_repositories import (
    MemberPhysicalMetaCompoundRepository,
)


class MemberPhysicalMeta(ValueObject):
    member_id: MemberID
    birth_year: PositiveInt
    gender: Gender
    body_shape: Optional[Meta]
    height: Optional[Meta]
    weight: Optional[Meta]
    physical_meta_repo: SkipJsonSchema[MemberPhysicalMetaCompoundRepository] = Field(exclude=True)
    birth_meta_repo: SkipJsonSchema[MemberBirthMetaCompoundRepository] = Field(exclude=True)

    def __init__(
        self,
        member_id: MemberID,
        gender: Optional[Gender] = None,
        birth_year: Optional[PositiveInt] = None,
        birth_meta_repo: MemberBirthMetaCompoundRepository = MemberBirthMetaCompoundRepository(),
    ):
        physical_meta_repo: MemberPhysicalMetaCompoundRepository = MemberPhysicalMetaCompoundRepository(
            member_id=member_id
        )

        super().__init__(
            member_id=member_id,
            birth_year=birth_year if birth_year else birth_meta_repo.find_birth_year_by(member_id=member_id),
            gender=gender if gender else birth_meta_repo.find_gender_by(member_id=member_id),
            body_shape=physical_meta_repo.find_by_type(PhysicalMetaType.BODY_SHAPE),
            height=physical_meta_repo.find_by_type(PhysicalMetaType.HEIGHT),
            weight=physical_meta_repo.find_by_type(PhysicalMetaType.WEIGHT),
            physical_meta_repo=physical_meta_repo,
            birth_meta_repo=birth_meta_repo,
        )

    @classmethod
    def get_instance(cls, member_id: MemberID, gender: Gender, birth_year: PositiveInt) -> Self:
        member_meta: MemberPhysicalMeta = cls(member_id=member_id, gender=gender, birth_year=birth_year)
        member_meta.register_gender_and_birth_year(gender=gender, birth_year=birth_year)
        return member_meta

    def register_gender_and_birth_year(self, gender: Gender, birth_year: PositiveInt) -> None:
        self.birth_meta_repo.create_or_update_birth_year_and_gender(
            self.member_id, gender=gender, birth_year=birth_year
        )

    def update_physical_meta(self, meta_id: PositiveInt, meta_type: PhysicalMetaType) -> Self:
        new_physical_meta: Meta
        if meta_type == PhysicalMetaType.HEIGHT:
            new_physical_meta = self.physical_meta_repo.create_or_update_height_meta(
                member_id=self.member_id, height_meta_id=meta_id
            )
            self.height = new_physical_meta
        elif meta_type == PhysicalMetaType.WEIGHT:
            new_physical_meta = self.physical_meta_repo.create_or_update_weight_meta(
                member_id=self.member_id, weight_meta_id=meta_id
            )
            self.weight = new_physical_meta
        else:
            new_physical_meta = self.physical_meta_repo.create_or_update_body_shape_meta(
                member_id=self.member_id, body_shape_meta_id=meta_id
            )
            self.body_shape = new_physical_meta

        return self
