from typing import Optional

from ninja import Schema
from pydantic import StrictBool

from application.matching_context.domain_layer.value_object.friend import Friend


class MatchingExcludeFriendsSchema(Schema):
    is_exclude: StrictBool
    exclude_friends: Optional[list[Friend]] = None
