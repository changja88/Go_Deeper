from typing import Optional

from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import (
    MULTI_SELECTION_PREFERENCE_META,
    SINGLE_SELECTION_PREFERENCE_META,
    PreferenceMetaType,
)
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.member_preference_meta_repositories import (
    MemberPreferenceMetaCompoundRepository,
)


class MemberPreferenceMeta(ValueObject):
    member_id: MemberID
    smoking: Optional[Meta]
    alcohol: Optional[Meta]
    religion: Optional[Meta]
    MBTI: Optional[Meta]
    hobby: list[Meta]
    date_style: list[Meta]
    key_word: list[Meta]
    growth: list[Meta]
    repo: SkipJsonSchema[MemberPreferenceMetaCompoundRepository] = Field(exclude=True)

    def __init__(
        self,
        member_id: MemberID,
    ):
        repo: MemberPreferenceMetaCompoundRepository = MemberPreferenceMetaCompoundRepository(member_id=member_id)
        super().__init__(
            member_id=member_id,
            smoking=repo.find_by_type(PreferenceMetaType.SMOKING),
            alcohol=repo.find_by_type(PreferenceMetaType.ALCOHOL),
            religion=repo.find_by_type(PreferenceMetaType.RELIGION),
            MBTI=repo.find_by_type(PreferenceMetaType.MBTI),
            hobby=repo.find_by_type(PreferenceMetaType.HOBBY),
            date_style=repo.find_by_type(PreferenceMetaType.DATE_STYLE),
            key_word=repo.find_by_type(PreferenceMetaType.KEYWORD),
            growth=repo.find_by_type(PreferenceMetaType.GROWTH),
            repo=repo,
        )

    def add_preference_metas(self, meta_ids: list[PositiveInt], meta_type: PreferenceMetaType) -> None:
        self.repo.delete_same_type_meta_by(meta_type=meta_type, member_id=MemberID(self.member_id))
        if meta_type in SINGLE_SELECTION_PREFERENCE_META:
            new_preference_meta = self.repo.create(meta_id=meta_ids[0], member_id=MemberID(self.member_id))
            self._allocate_preference_meta(new_preference_meta, meta_type)
        elif meta_type in MULTI_SELECTION_PREFERENCE_META:
            new_preference_meta_list: list[Meta] = list()
            for meta_id in meta_ids:
                new_preference_meta_list.append(self.repo.create(meta_id=meta_id, member_id=MemberID(self.member_id)))
            self._allocate_preference_metas(new_preference_meta_list, meta_type)

    def _allocate_preference_meta(self, preference_meta: Meta, meta_type: PreferenceMetaType) -> None:
        if meta_type == PreferenceMetaType.SMOKING:
            self.smoking = preference_meta
        elif meta_type == PreferenceMetaType.ALCOHOL:
            self.alcohol = preference_meta
        elif meta_type == PreferenceMetaType.RELIGION:
            self.religion = preference_meta
        elif meta_type == PreferenceMetaType.MBTI:
            self.MBTI = preference_meta

    def _allocate_preference_metas(self, preference_metas: list[Meta], meta_type: PreferenceMetaType) -> None:
        if meta_type == PreferenceMetaType.HOBBY:
            self.hobby = preference_metas
        elif meta_type == PreferenceMetaType.DATE_STYLE:
            self.date_style = preference_metas
        elif meta_type == PreferenceMetaType.KEYWORD:
            self.key_word = preference_metas
        elif meta_type == PreferenceMetaType.GROWTH:
            self.growth = preference_metas
