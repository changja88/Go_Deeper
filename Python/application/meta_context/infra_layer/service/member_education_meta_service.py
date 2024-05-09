from pydantic import PositiveInt

from applications.common.type import MemberID
from application.meta_context.context_layer.publisher.meta_register_event_pub import (
    MetaRegisterEventPublisher,
)
from application.meta_context.domain_layer.entity.member_education_meta import (
    MemberEducationMeta,
)
from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.lookup_education_meta_repositories import (
    EducationMetaLookupCompoundRepository,
)


class MemberEducationMetaService:
    meta_lookup_repo: EducationMetaLookupCompoundRepository
    CUSTOM_INPUT_PREFIX = "직접입력"

    def __init__(
        self,
        meta_lookup_repo: EducationMetaLookupCompoundRepository = EducationMetaLookupCompoundRepository(),
    ):
        self.meta_lookup_repo = meta_lookup_repo

    def find_by_member_id(self, member_id: MemberID) -> MemberEducationMeta:
        return MemberEducationMeta(member_id=member_id)

    def register_member_custom_education_meta(
        self, member_id: MemberID, meta_type: UniversityType, custom_value: str
    ) -> MemberEducationMeta:
        member_education_meta: MemberEducationMeta = MemberEducationMeta(member_id=member_id)
        created_meta: Meta = self.meta_lookup_repo.get_or_create_custom_meta(
            custom_value=custom_value, education_meta_type=meta_type
        )
        member_education_meta.register_university(meta_id=created_meta.id)
        self._publish_education_meta_register_event(member_education_meta=member_education_meta)
        return member_education_meta

    def register_member_education_meta(self, member_id: MemberID, meta_id: PositiveInt) -> MemberEducationMeta:
        member_education_meta: MemberEducationMeta = MemberEducationMeta(member_id=member_id)
        member_education_meta.register_university(meta_id=meta_id)
        self._publish_education_meta_register_event(member_education_meta=member_education_meta)
        return member_education_meta

    def _publish_education_meta_register_event(self, member_education_meta: MemberEducationMeta) -> None:
        if education_meta := member_education_meta.university:
            MetaRegisterEventPublisher.publish_education_meta_register_event(
                member_id=member_education_meta.member_id, education_meta_tear=education_meta.tear
            )
