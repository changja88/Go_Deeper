from typing import Optional, Self

from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import CertifiableMeta
from application.meta_context.infra_layer.repository.member_finance_meta_repositories import (
    MemberFinanceMetaCompoundRepository,
)


class MemberFinanceMeta(ValueObject):
    member_id: MemberID
    income: Optional[CertifiableMeta]
    job: Optional[CertifiableMeta]
    company: Optional[CertifiableMeta]
    asset: Optional[CertifiableMeta]
    car_brand: Optional[CertifiableMeta]
    car_price: Optional[CertifiableMeta]
    family_asset: Optional[CertifiableMeta]
    mother_job: Optional[CertifiableMeta]
    father_job: Optional[CertifiableMeta]
    repo: SkipJsonSchema[MemberFinanceMetaCompoundRepository] = Field(exclude=True)

    def __init__(self, member_id: MemberID):
        repo: MemberFinanceMetaCompoundRepository = MemberFinanceMetaCompoundRepository(member_id=member_id)
        super().__init__(
            member_id=member_id,
            income=repo.find_by_type(FinanceMetaType.INCOME),
            job=repo.find_by_type(FinanceMetaType.JOB),
            company=repo.find_by_type(FinanceMetaType.COMPANY),
            asset=repo.find_by_type(FinanceMetaType.ASSET),
            car_brand=repo.find_by_type(FinanceMetaType.CAR_BRAND),
            car_price=repo.find_by_type(FinanceMetaType.CAR_PRICE),
            family_asset=repo.find_by_type(FinanceMetaType.FAMILY_ASSET),
            mother_job=repo.find_by_type(FinanceMetaType.MOTHER_JOB),
            father_job=repo.find_by_type(FinanceMetaType.FATHER_JOB),
            repo=repo,
        )

    def register_meta(self, meta_id: PositiveInt, meta_type: FinanceMetaType) -> Self:
        new_finance_meta: CertifiableMeta = self.repo.update_or_create(
            meta_id=meta_id, member_id=self.member_id, meta_type=meta_type
        )
        self._allocate_meta([new_finance_meta])
        return self

    def _allocate_meta(self, meta_list: list[CertifiableMeta]) -> None:
        for meta in meta_list:
            if meta.type == FinanceMetaType.INCOME:
                self.income = meta
            elif meta.type == FinanceMetaType.JOB:
                self.job = meta
            elif meta.type == FinanceMetaType.COMPANY:
                self.company = meta
            elif meta.type == FinanceMetaType.ASSET:
                self.asset = meta
            elif meta.type == FinanceMetaType.CAR_BRAND:
                self.car_brand = meta
            elif meta.type == FinanceMetaType.CAR_PRICE:
                self.car_price = meta
            elif meta.type == FinanceMetaType.FAMILY_ASSET:
                self.family_asset = meta
            elif meta.type == FinanceMetaType.MOTHER_JOB:
                self.mother_job = meta
            elif meta.type == FinanceMetaType.FATHER_JOB:
                self.father_job = meta
