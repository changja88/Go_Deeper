from typing import Optional

from applications.common.type import MemberID
from application.member_context.context_layer.subscriber.member_address_reqeust_event_sub import (
    MemberAddressRequestEventSubscriber,
)
from applications.member.domain_layer.entity.member_address import MemberAddress
from application.meta_context.context_layer.subscriber.member_meta_request_event_sub import (
    MemberMetaRequestEventSubscriber,
)
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


class MemberMetaRequestEventPublisher:

    @classmethod
    def publish_member_education_meta_request_event(cls, member_id: MemberID) -> MemberEducationMeta:
        return MemberMetaRequestEventSubscriber.subscribe_member_education_meta_request_event(member_id=member_id)

    @classmethod
    def publish_member_finance_meta_request_event(cls, member_id: MemberID) -> MemberFinanceMeta:
        return MemberMetaRequestEventSubscriber.subscribe_member_finance_meta_request_event(member_id=member_id)

    @classmethod
    def publish_member_photo_meta_request_event(cls, member_id: MemberID) -> MemberPhotoMeta:
        return MemberMetaRequestEventSubscriber.subscribe_member_photo_meta_request_event(member_id=member_id)

    @classmethod
    def publish_member_physical_meta_request_event(cls, member_id: MemberID) -> MemberPhysicalMeta:
        return MemberMetaRequestEventSubscriber.subscribe_member_physical_meta_request_event(member_id=member_id)

    @classmethod
    def publish_member_preference_meta_request_event(cls, member_id: MemberID) -> MemberPreferenceMeta:
        return MemberMetaRequestEventSubscriber.publish_member_preference_meta_request_event(member_id=member_id)

    @classmethod
    def publish_member_address_request_event(cls, member_id: MemberID) -> Optional[MemberAddress]:
        return MemberAddressRequestEventSubscriber.subscribe_address_request_event(member_id=member_id)
