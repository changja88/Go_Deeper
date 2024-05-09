from typing import Optional

from pydantic import BaseModel

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.type import MemberID
from applications.member.domain_layer.entity.member import Member
from application.member_context.infra_layer.django.models import MemberORM


class MemberFindCondition(BaseModel):
    name: str
    phone_number: str


class MemberReadRepository:
    def find_by_cond(self, con: MemberFindCondition) -> Optional[Member]:
        member: Optional[Member] = get_obj_or_none(MemberORM, **con.model_dump())
        return member

    def find_by_member_id(self, member_id: MemberID) -> Optional[Member]:
        if member_orm := get_obj_or_none(MemberORM, id=member_id):
            member: Member = Member.model_validate(member_orm)
            return member
        return None

    def find_by_nick_name(self, nickname: str) -> Optional[Member]:
        if member_orm := get_obj_or_none(MemberORM, nickname=nickname):
            member: Member = Member.model_validate(member_orm)
            return member
        return None


class MemberWriteRepository:
    def create(self, member: Member) -> Member:
        created_member_orm: MemberORM = MemberORM.objects.create(**member.model_dump())
        member = Member.model_validate(created_member_orm)
        return member

    def update(self, member: Member) -> Member:
        updated_member_orm, _ = MemberORM.objects.update_or_create(id=member.id, defaults=member.model_dump())
        member = Member.model_validate(updated_member_orm)
        return member


class MemberCompoundRepository(MemberReadRepository, MemberWriteRepository):
    pass
