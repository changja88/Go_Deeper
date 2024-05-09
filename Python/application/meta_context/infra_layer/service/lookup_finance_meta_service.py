from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import Meta
from application.meta_context.infra_layer.repository.lookup_finance_meta_repositories import (
    FinanceMetaLookupCompoundRepository,
)


class FinanceMetaLookupService:
    repo: FinanceMetaLookupCompoundRepository
    CUSTOM_INPUT_PREFIX = "직접입력"

    def __init__(self, repo: FinanceMetaLookupCompoundRepository = FinanceMetaLookupCompoundRepository()):
        self.repo = repo

    def find_by_meta_type(self, meta_type: FinanceMetaType) -> list[Meta]:
        return self.repo.find_all_by_type(meta_type=FinanceMetaType(meta_type))

    def search_by(self, meta_type: FinanceMetaType, search_text: str) -> list[Meta]:
        return self.repo.search_meta_list_by(search_text=search_text, meta_type=meta_type)
