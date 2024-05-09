from pydantic import PositiveInt

from applications.common.enum import Gender
from applications.common.type import MemberID
from application.meta_context.infra_layer.service.member_meta_service import (
    MemberMetaService,
    RegisterEvent,
)


class RegisterEventSubscriber:
    @classmethod
    def subscribe_birth_meta_register_event(self, member_id: MemberID, birth_year: PositiveInt, gender: Gender) -> None:
        MemberMetaService().register_birth_meta_from_register_event(
            register_event=RegisterEvent(member_id=member_id, birth_year=birth_year, gender=gender)
        )
