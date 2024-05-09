from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_date_test_meta import (
    MemberDateTestMeta,
)
from application.meta_context.domain_layer.value_object.meta.date_test import DateTest
from application.meta_context.infra_layer.service.lookup_date_test_meta_service import (
    DateTestMetaLookupService,
)
from application.meta_context.infra_layer.service.member_date_test_meta_service import (
    MemberDateTestMetaService,
)


class DateTestMetaRequestEventSubscriber:
    @classmethod
    def subscribe_member_date_test_meta_request_event(cls, member_id: MemberID) -> MemberDateTestMeta:
        return MemberDateTestMetaService().find_by(member_id=member_id)

    @classmethod
    def subscribe_date_test_request_event(cls) -> DateTest:
        return DateTestMetaLookupService().find_all()
