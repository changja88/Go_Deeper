from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.lookup_education_meta_repositories import (
    EducationMetaLookupCompoundRepository,
)


class EducationMetaLookupService:
    repo: EducationMetaLookupCompoundRepository

    def __init__(self, repo: EducationMetaLookupCompoundRepository = EducationMetaLookupCompoundRepository()):
        self.repo = repo

    def find_all_by_meta_type(self, meta_type: UniversityType) -> list[Meta]:
        return self.repo.find_all_by_meta_type(meta_type=meta_type)

    def search_by(self, meta_type: UniversityType, search_text: str) -> list[Meta]:
        return self.repo.search_meta_list_by(meta_type=meta_type, search_text=search_text)
