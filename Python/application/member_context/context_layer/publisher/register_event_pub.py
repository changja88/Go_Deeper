from pydantic import PositiveInt

from applications.common.enum import Gender
from applications.common.type import MemberID
from application.meta_context.context_layer.subscriber.register_event_sub import (
    RegisterEventSubscriber,
)


class RegisterEventPublisher:
    @classmethod
    def publish_birth_year_register_event(self, member_id: MemberID, birth_year: PositiveInt, gender: Gender) -> None:
        RegisterEventSubscriber.subscribe_birth_meta_register_event(
            member_id=member_id, birth_year=birth_year, gender=gender
        )
