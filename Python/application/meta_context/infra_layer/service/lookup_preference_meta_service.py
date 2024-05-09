from typing import Optional

from application.meta_context.domain_layer.meta_enum import PreferenceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.lookup_preference_meta_repositories import (
    PreferenceMetaCompoundRepository,
)


class PreferenceMetaLookupService:
    repo: PreferenceMetaCompoundRepository

    def __init__(self, repo: PreferenceMetaCompoundRepository = PreferenceMetaCompoundRepository()):
        self.repo = repo

    def find_meta_by_type(self, meta_type: PreferenceMetaType) -> Optional[list[Meta]]:
        if meta_list := self.repo.find_by_type(meta_type=meta_type):
            return meta_list
        return None
