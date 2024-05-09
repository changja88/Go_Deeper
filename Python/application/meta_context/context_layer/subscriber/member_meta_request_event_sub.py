from applications.common.enum import Gender
from applications.common.type import MemberID
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
from application.meta_context.infra_layer.service.member_education_meta_service import (
    MemberEducationMetaService,
)
from application.meta_context.infra_layer.service.member_finance_meta_service import (
    MemberFinanceMetaService,
)
from application.meta_context.infra_layer.service.member_meta_service import (
    MemberMetaService,
)
from application.meta_context.infra_layer.service.member_photo_service import (
    MemberPhotoService,
)
from application.meta_context.infra_layer.service.member_preference_meta_service import (
    MemberPreferenceMetaService,
)


class MemberMetaRequestEventSubscriber:

    @classmethod
    def subscribe_member_education_meta_request_event(cls, member_id: MemberID) -> MemberEducationMeta:
        return MemberEducationMetaService().find_by_member_id(member_id=member_id)

    @classmethod
    def subscribe_member_finance_meta_request_event(cls, member_id: MemberID) -> MemberFinanceMeta:
        return MemberFinanceMetaService().find_by_member_id(member_id=member_id)

    @classmethod
    def subscribe_member_photo_meta_request_event(cls, member_id: MemberID) -> MemberPhotoMeta:
        return MemberPhotoService().find_by(member_id=member_id)

    @classmethod
    def subscribe_member_physical_meta_request_event(cls, member_id: MemberID) -> MemberPhysicalMeta:
        return MemberMetaService().find_by(member_id=member_id)

    @classmethod
    def publish_member_preference_meta_request_event(cls, member_id: MemberID) -> MemberPreferenceMeta:
        return MemberPreferenceMetaService(member_id=member_id).find_by_memer_id(member_id=member_id)

    @classmethod
    def subscribe_member_gender_request_event(cls, member_id: MemberID) -> Gender:
        return MemberMetaService().find_by(member_id=member_id).gender
