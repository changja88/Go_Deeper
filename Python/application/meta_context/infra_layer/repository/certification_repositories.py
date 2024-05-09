from typing import Optional

from pydantic import PositiveInt

from applications.common.django.django_model_util import get_obj_or_none
from application.meta_context.domain_layer.meta_enum import CensorStatus
from application.meta_context.infra_layer.django_meta.models.certification_orm import (
    CertificationORM,
)


class CertificationReadRepository:
    def find_rejected_reason_and_censor_status(
        self, certification_id: PositiveInt
    ) -> tuple[Optional[str], Optional[CensorStatus]]:
        certification_orm: Optional[CertificationORM]
        if certification_orm := get_obj_or_none(CertificationORM, id=certification_id):
            return certification_orm.rejected_reason, CensorStatus(certification_orm.censor_status)
        return None, None


class CertificationWriteRepository:
    pass


class CertificationCompoundRepository(CertificationReadRepository, CertificationWriteRepository):
    pass
