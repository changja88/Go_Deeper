from applications.common.type import MemberID
from application.meta_context.context_layer.subscriber.date_test_meta_request_event_sub import (
    DateTestMetaRequestEventSubscriber,
)
from application.meta_context.domain_layer.entity.member_date_test_meta import (
    MemberDateTestMeta,
)
from application.meta_context.domain_layer.value_object.meta.date_test import DateTest


class DateTestMetaRequestEventPublisher:
    @classmethod
    def publish_member_date_test_meta_request_event(self, member_id: MemberID) -> MemberDateTestMeta:
        return DateTestMetaRequestEventSubscriber.subscribe_member_date_test_meta_request_event(member_id=member_id)

    @classmethod
    def publish_date_test_request_event(cls) -> DateTest:
        return DateTestMetaRequestEventSubscriber.subscribe_date_test_request_event()
