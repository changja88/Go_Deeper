from typing import Optional

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.matching_context.context_layer.member_address_request_event_pub import (
    MemberAddressRequestEventPublisher,
)
from application.matching_context.context_layer.member_meta_request_event_pub import (
    MemberMetaRequestEventPublisher,
)
from application.matching_context.context_layer.member_request_event_pub import (
    MemberRequestEventPublisher,
)
from applications.member.domain_layer.entity.member import Member
from applications.member.domain_layer.entity.member_address import MemberAddress
from application.meta_context.domain_layer.entity.member_education_meta import (
    MemberEducationMeta,
)
from application.meta_context.domain_layer.entity.member_finance_meta import (
    MemberFinanceMeta,
)
from application.meta_context.domain_layer.entity.member_photo_meta import (
    MemberPhotoMeta,
)
from application.meta_context.domain_layer.entity.member_physical_meta import (
    MemberPhysicalMeta,
)
from application.meta_context.domain_layer.entity.member_preference_meta import (
    MemberPreferenceMeta,
)
from application.meta_context.domain_layer.value_object.meta.photo import Photo


class MatchingCard(ValueObject):
    nickname: Optional[str]
    introduction: Optional[str]
    photo: Optional[Photo]
    member_education_meta: Optional[MemberEducationMeta]
    member_finance_meta: Optional[MemberFinanceMeta]
    member_physical_meta: Optional[MemberPhysicalMeta]
    member_preference_meta: Optional[MemberPreferenceMeta]
    member_address: Optional[MemberAddress]

    def __init__(self, member_id: MemberID) -> None:
        member: Optional[Member] = MemberRequestEventPublisher.publish_member_request_event(member_id=member_id)
        member_photo_meta: MemberPhotoMeta = MemberMetaRequestEventPublisher.publish_member_photo_meta_request_event(
            member_id=member_id
        )
        super().__init__(
            nickname=member.unique_info.nickname if member else None,
            introduction=member.introduction if member else None,
            photo=member_photo_meta.find_main_photo() if member_photo_meta else None,
            member_education_meta=MemberMetaRequestEventPublisher.publish_member_education_meta_request_event(
                member_id=member_id
            ),
            member_finance_meta=MemberMetaRequestEventPublisher.publish_member_finance_meta_request_event(
                member_id=member_id
            ),
            member_physical_meta=MemberMetaRequestEventPublisher.publish_member_physical_meta_request_event(
                member_id=member_id
            ),
            member_preference_meta=MemberMetaRequestEventPublisher.publish_member_preference_meta_request_event(
                member_id=member_id
            ),
            member_address=MemberAddressRequestEventPublisher.publish_address_request_event(member_id=member_id),
        )
