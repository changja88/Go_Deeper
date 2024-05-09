from typing import Optional

from pydantic import PositiveInt

from applications.common.enum import Gender
from applications.common.type import MemberID
from application.meta_context.infra_layer.django_meta.models.birth_meta_orm import (
    MemberBirthMetaORM,
)


class MemberBirthMetaReadRepository:
    def find_birth_year_by(self, member_id: MemberID) -> Optional[PositiveInt]:
        member_physical_meta_orm: MemberBirthMetaORM = MemberBirthMetaORM.objects.get(member_id=member_id)
        return member_physical_meta_orm.birth_year

    def find_gender_by(self, member_id: MemberID) -> Optional[Gender]:
        member_physical_meta_orm: MemberBirthMetaORM = MemberBirthMetaORM.objects.get(member_id=member_id)
        return Gender(member_physical_meta_orm.gender)


class MemberBirthMetaWriteRepository:
    def create_or_update_birth_year_and_gender(self, member_id: MemberID, birth_year: PositiveInt, gender: str) -> None:
        MemberBirthMetaORM.objects.update_or_create(
            member_id=member_id, defaults={"birth_year": birth_year, "gender": gender}
        )


class MemberBirthMetaCompoundRepository(MemberBirthMetaReadRepository, MemberBirthMetaWriteRepository):
    pass
