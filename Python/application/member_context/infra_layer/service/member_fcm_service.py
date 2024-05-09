from typing import Optional

from applications.common.type import MemberID
from applications.member.domain_layer.entity.member_fcm import MemberFCM
from application.member_context.infra_layer.repository.member_fcm_repositories import (
    MemberFCMCompoundRepository,
)


class MemberFCMService:
    repo: MemberFCMCompoundRepository

    def __init__(self, repo: MemberFCMCompoundRepository = MemberFCMCompoundRepository()):
        self.repo = repo

    def _find_by(self, member_id: MemberID) -> Optional[MemberFCM]:
        return self.repo.find_by(member_id=member_id)

    def register(self, member_id: MemberID, fcm_token: str, device_info: str) -> MemberFCM:
        if member_fcm := self._find_by(member_id=member_id):
            if member_fcm == fcm_token:
                return member_fcm
        member_fcm = MemberFCM(member_id=member_id, fcm_token=fcm_token, device_info=device_info)
        return self.repo.update_or_create(member_fcm)
