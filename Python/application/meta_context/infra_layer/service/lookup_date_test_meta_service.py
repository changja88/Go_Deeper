from application.meta_context.domain_layer.value_object.meta.date_test import DateTest
from application.meta_context.infra_layer.repository.lookup_date_test_meta_repositories import (
    DateTestMetaLookupCompoundRepository,
)


class DateTestMetaLookupService:
    repo: DateTestMetaLookupCompoundRepository

    def __init__(self, repo: DateTestMetaLookupCompoundRepository = DateTestMetaLookupCompoundRepository()):
        self.repo = repo

    def find_all(self) -> DateTest:
        return self.repo.find_all()
