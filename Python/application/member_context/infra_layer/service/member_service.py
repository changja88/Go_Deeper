from typing import Optional

from applications.common.type import MemberID
from applications.member.domain_layer.entity.member import Member
from application.member_context.infra_layer.repository.member_repositories import (
    MemberCompoundRepository,
)


class MemberService:
    repo: MemberCompoundRepository

    def __init__(self, repo: MemberCompoundRepository = MemberCompoundRepository()):
        self.repo = repo

    def find_by_member_id(self, member_id: MemberID) -> Optional[Member]:
        return self.repo.find_by_member_id(member_id=member_id)

    def update_member_introduction(self, member: Member, new_introduction: str) -> Member:
        member.introduction = new_introduction
        return self.repo.update(member=member)
