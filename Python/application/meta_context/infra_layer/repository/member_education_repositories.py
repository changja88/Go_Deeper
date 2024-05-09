from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import get_obj_or_none
from applications.common.type import MemberID
from application.meta_context.domain_layer.meta_enum import UniversityType
from application.meta_context.domain_layer.value_object.certification.meta_certification import (
    Certification,
)
from application.meta_context.domain_layer.value_object.meta.meta import CertifiableMeta
from application.meta_context.infra_layer.django_meta.models import (
    MemberEducationMetaORM,
)


class MemberEducationMetaReadRepository:
    def find_by(self, member_id: MemberID) -> Optional[CertifiableMeta]:
        member_education_meta_orm: Optional[MemberEducationMetaORM] = get_obj_or_none(
            MemberEducationMetaORM, member_id=member_id
        )
        if member_education_meta_orm:
            return CertifiableMeta(
                id=member_education_meta_orm.education_meta.id,
                value=member_education_meta_orm.education_meta.value,
                type=UniversityType(member_education_meta_orm.education_meta.type),
                tear=member_education_meta_orm.education_meta.tear,
                certification=Certification(id=member_education_meta_orm.id),
            )

        return None


class MemberEducationMetaWriteRepository:
    def update_or_create(self, member_id: MemberID, meta_id: PositiveInt) -> CertifiableMeta:
        member_education_meta_orm, _ = MemberEducationMetaORM.objects.update_or_create(
            member_id=member_id, defaults={"education_meta_id": meta_id}
        )
        return CertifiableMeta(
            id=member_education_meta_orm.education_meta.id,
            type=UniversityType(member_education_meta_orm.education_meta.type),
            value=member_education_meta_orm.education_meta.value,
            tear=member_education_meta_orm.education_meta.tear,
            certification=Certification(id=member_education_meta_orm.id),
        )


class MemberEducationMetaCompoundRepository(MemberEducationMetaReadRepository, MemberEducationMetaWriteRepository): ...
