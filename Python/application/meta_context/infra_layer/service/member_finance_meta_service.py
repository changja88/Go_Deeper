from typing import Optional

from pydantic import BaseModel, PositiveInt

from applications.common.type import MemberID
from application.evaluation_context.domain_layer.evaluation_enum import (
    ASSET_EVALUATION_TYPE_SOURCE_SET,
    BACKGROUND_EVALUATION_TYPE_SOURCE_SET,
    WORK_EVALUATION_TYPE_SOURCE_SET,
)
from application.meta_context.context_layer.publisher.meta_register_event_pub import (
    MetaRegisterEventPublisher,
)
from application.meta_context.domain_layer.entity.member_finance_meta import (
    MemberFinanceMeta,
)
from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.domain_layer.value_object.meta.meta import (
    CertifiableMeta,
    Meta,
)
from application.meta_context.infra_layer.repository.lookup_finance_meta_repositories import (
    FinanceMetaLookupCompoundRepository,
)


class MemberFinanceMetaInput(BaseModel):
    member_id: MemberID
    meta_id: PositiveInt
    custom_value: Optional[str]


class MemberFinanceMetaService:
    meta_lookup_repo: FinanceMetaLookupCompoundRepository
    CUSTOM_INPUT_PREFIX = "직접입력"

    def __init__(self, meta_lookup_repo: FinanceMetaLookupCompoundRepository = FinanceMetaLookupCompoundRepository()):
        self.meta_lookup_repo = meta_lookup_repo

    def find_by_member_id(self, member_id: MemberID) -> MemberFinanceMeta:
        return MemberFinanceMeta(member_id=member_id)

    def _create_custom_meta(self, meta_type: FinanceMetaType, custom_value: str) -> Meta:
        return self.meta_lookup_repo.get_or_create_custom_meta(meta_type=meta_type, custom_value=custom_value)

    def register_custom_member_finance_meta(
        self, member_id: MemberID, meta_type: FinanceMetaType, custom_value: str
    ) -> MemberFinanceMeta:
        member_finance_meta: MemberFinanceMeta = MemberFinanceMeta(member_id=member_id)
        created_custom_meta: Meta = self._create_custom_meta(meta_type=meta_type, custom_value=custom_value)
        member_finance_meta.register_meta(
            meta_id=created_custom_meta.id,
            meta_type=FinanceMetaType(created_custom_meta.type),
        )
        self._publish_finance_meta_register_event(
            member_finance_meta=member_finance_meta,
            register_finance_meta_type=FinanceMetaType(created_custom_meta.type),
        )
        return member_finance_meta

    def register_member_finance_meta(self, member_id: MemberID, meta_id: PositiveInt) -> MemberFinanceMeta:
        member_finance_meta: MemberFinanceMeta = MemberFinanceMeta(member_id=member_id)
        new_finance_meta: Optional[CertifiableMeta]
        if new_finance_meta := self.meta_lookup_repo.find_by_id(meta_id):
            member_finance_meta.register_meta(
                meta_id=new_finance_meta.id,
                meta_type=FinanceMetaType(new_finance_meta.type),
            )
            self._publish_finance_meta_register_event(
                member_finance_meta=member_finance_meta,
                register_finance_meta_type=FinanceMetaType(new_finance_meta.type),
            )
        return member_finance_meta

    def _publish_finance_meta_register_event(
        self, member_finance_meta: MemberFinanceMeta, register_finance_meta_type: FinanceMetaType
    ) -> None:
        if register_finance_meta_type == FinanceMetaType.INCOME:
            if income_meta := member_finance_meta.income:
                MetaRegisterEventPublisher.publish_income_meta_register_event(
                    member_id=member_finance_meta.member_id, income_meta_tear=income_meta.tear
                )
        if register_finance_meta_type in WORK_EVALUATION_TYPE_SOURCE_SET:
            self._publish_work_evaluation_meta_register_event(member_finance_meta=member_finance_meta)
        elif register_finance_meta_type in ASSET_EVALUATION_TYPE_SOURCE_SET:
            self._publish_asset_evaluation_meta_register_event(member_finance_meta=member_finance_meta)
        elif register_finance_meta_type in BACKGROUND_EVALUATION_TYPE_SOURCE_SET:
            self._publish_background_evaluation_meta_register_event(member_finance_meta=member_finance_meta)

    def _publish_background_evaluation_meta_register_event(self, member_finance_meta: MemberFinanceMeta) -> None:
        MetaRegisterEventPublisher.publish_background_meta_register_event(
            member_id=member_finance_meta.member_id,
            family_asset_meta_tear=(
                member_finance_meta.family_asset.tear if member_finance_meta.family_asset else None
            ),
            father_job_meta_tear=(member_finance_meta.father_job.tear if member_finance_meta.father_job else None),
            mother_job_meta_tear=(member_finance_meta.mother_job.tear if member_finance_meta.mother_job else None),
        )

    def _publish_work_evaluation_meta_register_event(self, member_finance_meta: MemberFinanceMeta) -> None:
        MetaRegisterEventPublisher.publish_work_meta_register_event(
            member_id=member_finance_meta.member_id,
            job_meta_tear=(member_finance_meta.job.tear if member_finance_meta.job else None),
            company_meta_tear=(member_finance_meta.company.tear if member_finance_meta.company else None),
        )

    def _publish_asset_evaluation_meta_register_event(self, member_finance_meta: MemberFinanceMeta) -> None:
        MetaRegisterEventPublisher.publish_asset_meta_register_event(
            member_id=member_finance_meta.member_id,
            asset_meta_tear=(member_finance_meta.asset.tear if member_finance_meta.asset else None),
            car_price_meta_tear=(member_finance_meta.car_price.tear if member_finance_meta.car_price else None),
        )
