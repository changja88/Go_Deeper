from pydantic import PositiveInt

from applications.common.type import MemberID
from application.meta_context.domain_layer.entity.member_preference_meta import (
    MemberPreferenceMeta,
)
from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.meta_context.infra_layer.repository.lookup_preference_meta_repositories import (
    PreferenceMetaCompoundRepository,
)
from application.meta_context.infra_layer.repository.member_preference_meta_repositories import (
    MemberPreferenceMetaCompoundRepository,
)


class MemberPreferenceMetaService:
    member_meta_repo: MemberPreferenceMetaCompoundRepository
    meta_lookup_repo: PreferenceMetaCompoundRepository

    def __init__(self, member_id: MemberID):
        self.member_meta_repo = MemberPreferenceMetaCompoundRepository(member_id=member_id)
        self.meta_lookup_repo = PreferenceMetaCompoundRepository()

    def find_by_memer_id(self, member_id: MemberID) -> MemberPreferenceMeta:
        return MemberPreferenceMeta(member_id=member_id)

    def register_member_preference_meta(
        self,
        member_id: MemberID,
        preference_meta_id_list: list[PositiveInt],
        preference_meta_type: PreferenceMetaType,
    ) -> MemberPreferenceMeta:
        member_preference_meta: MemberPreferenceMeta = MemberPreferenceMeta(member_id=member_id)
        member_preference_meta.add_preference_metas(meta_ids=preference_meta_id_list, meta_type=preference_meta_type)
        return member_preference_meta
