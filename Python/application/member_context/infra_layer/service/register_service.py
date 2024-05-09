import uuid
from typing import Optional

from pydantic import StrictBool

from applications.member.domain_layer.entity.member import Member
from applications.member.domain_layer.value_object.enum import MemberStatus
from applications.member.domain_layer.value_object.permission import (
    AdminPermission,
)
from applications.member.domain_layer.value_object.unique_info import UniqueInfo
from application.member_context.infra_layer.repository.member_repositories import (
    MemberCompoundRepository,
    MemberFindCondition,
)


class RegisterService:
    repo: MemberCompoundRepository

    def __init__(self, repo: MemberCompoundRepository = MemberCompoundRepository()):
        self.repo = repo

    def register(self, unique_info: UniqueInfo) -> Member:
        member: Member = Member(
            unique_info=unique_info,
            permission=AdminPermission(),
            status=MemberStatus.REGISTERED,
            friend_code=str(uuid.uuid4())[:6],
        )
        member = self.repo.create(member=member)
        return member

    def find_by_cond(self, find_cond: MemberFindCondition) -> Optional[Member]:
        if member := self.repo.find_by_cond(con=find_cond):
            return member
        return None

    def is_nickname_exists(self, nickname: str) -> StrictBool:
        if self.repo.find_by_nick_name(nickname=nickname):
            return True
        else:
            return False
