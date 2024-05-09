from pydantic import PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID


class Friend(ValueObject):
    member_id: MemberID
    name: str
    phone_number: PositiveInt
