from application.meta_context.domain_layer.meta_enum import PhysicalMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.lookup_physical_meta_repositories import (
    PhysicalMetaLookupCompoundRepository,
)


class PhysicalMetaLookupService:
    repo: PhysicalMetaLookupCompoundRepository

    def __init__(self, repo: PhysicalMetaLookupCompoundRepository = PhysicalMetaLookupCompoundRepository()):
        self.repo = repo

    def find_meta_by_type(self, meta_type: PhysicalMetaType) -> list[Meta]:
        return self.repo.find_by_type(meta_type=meta_type)
