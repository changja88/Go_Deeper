from typing import Optional

from applications.member.domain_layer.value_object.address import AddressUnit
from application.member_context.infra_layer.repository.address_repositories import (
    AddressCompoundRepository,
)


class AddressLookupService:
    repo: AddressCompoundRepository

    def __init__(self, repo: AddressCompoundRepository = AddressCompoundRepository()):
        self.repo = repo

    def find_all_address(self, lv1_id: Optional[int]) -> list[AddressUnit] | None:
        if lv1_id:
            return self.repo.find_lv2_address(lv1_id=lv1_id)
        else:
            return self.repo.find_lv1_address()
