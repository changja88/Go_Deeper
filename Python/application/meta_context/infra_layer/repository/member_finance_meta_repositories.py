from typing import Optional

from django.utils.functional import cached_property
from pydantic import PositiveInt

from applications.common.django.django_model_util import get_list_or_none
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import FinanceMetaType
from application.meta_context.domain_layer.value_object.certification.meta_certification import (
    Certification,
)
from application.meta_context.domain_layer.value_object.meta.meta import CertifiableMeta
from application.meta_context.infra_layer.django_meta.models import MemberFinanceMetaORM


class MemberFinanceMetaReadRepository:
    member_id: MemberID

    def __init__(self, member_id: MemberID) -> None:
        self.member_id = member_id

    @cached_property
    def all_meta(self) -> list[CertifiableMeta]:
        member_finance_meta_list = []
        if member_finance_meta_orm_list := get_list_or_none(MemberFinanceMetaORM, member_id=self.member_id):
            member_finance_meta_orm: MemberFinanceMetaORM
            for member_finance_meta_orm in member_finance_meta_orm_list:
                member_finance_meta_list.append(
                    CertifiableMeta(
                        id=member_finance_meta_orm.finance_meta.id,
                        type=FinanceMetaType(member_finance_meta_orm.finance_meta.type),
                        value=member_finance_meta_orm.finance_meta.value,
                        tear=member_finance_meta_orm.finance_meta.tear,
                        certification=Certification(id=member_finance_meta_orm.id),
                    )
                )
        return member_finance_meta_list

    def find_by_type(self, finance_type: FinanceMetaType) -> Optional[CertifiableMeta]:
        finance_meta: CertifiableMeta
        for finance_meta in self.all_meta:
            if finance_meta.type == finance_type:
                return finance_meta
        return None


class MemberFinanceMetaWriteRepository:

    def update_or_create(
        self, meta_id: MemberID, member_id: PositiveInt, meta_type: FinanceMetaType
    ) -> CertifiableMeta:
        member_finance_meta_orm: MemberFinanceMetaORM
        member_finance_meta_orm, _ = MemberFinanceMetaORM.objects.update_or_create(
            member_id=member_id,
            finance_meta__type=meta_type,
            defaults={"finance_meta_id": meta_id, "member_id": member_id},
        )
        return CertifiableMeta(
            id=member_finance_meta_orm.finance_meta.id,
            type=FinanceMetaType(member_finance_meta_orm.finance_meta.type),
            value=member_finance_meta_orm.finance_meta.value,
            tear=member_finance_meta_orm.finance_meta.tear,
            certification=Certification(id=member_finance_meta_orm.id),
        )


class MemberFinanceMetaCompoundRepository(MemberFinanceMetaReadRepository, MemberFinanceMetaWriteRepository): ...
