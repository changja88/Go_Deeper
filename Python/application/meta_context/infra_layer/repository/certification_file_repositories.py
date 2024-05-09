from typing import Optional

from ninja import UploadedFile
from pydantic import PositiveInt

from applications.common.django.django_model_util import get_list_or_none
from application.meta_context.domain_layer.value_object.file import CertificationFile
from application.meta_context.infra_layer.django_meta.models.certification_orm import (
    CertificationFileORM,
)


class CertificationFileReadRepository:
    def find_all_by_id(self, certification_id: PositiveInt) -> list[CertificationFile]:
        certification_file_orm_list: Optional[list[CertificationFileORM]]
        certification_files: list[CertificationFile] = list()
        if certification_file_orm_list := get_list_or_none(
            CertificationFileORM, certification_id=certification_id, is_deleted=False
        ):
            for certification_file_orm in certification_file_orm_list:
                certification_files.append(
                    CertificationFile(
                        id=certification_file_orm.id,
                        file=certification_file_orm.file.url,
                        is_deleted=certification_file_orm.is_deleted,
                    )
                )
        return certification_files


class CertificationFileWriteRepository:
    def register_certification_files(
        self, certification_id: PositiveInt, files: list[UploadedFile]
    ) -> list[CertificationFile]:
        certification_files: list[CertificationFile] = list()
        for file in files:
            certification_file_orm: CertificationFileORM = CertificationFileORM.objects.create(
                certification_id=certification_id, file=file
            )
            certification_files.append(
                CertificationFile(
                    id=certification_file_orm.id,
                    file=certification_file_orm.file.url,
                    is_deleted=certification_file_orm.is_deleted,
                )
            )
        return certification_files

    def set_file_as_deleted(self, file_id: PositiveInt) -> None:
        CertificationFileORM.objects.filter(id=file_id).update(is_deleted=True)


class CertificationFileCompoundRepository(CertificationFileReadRepository, CertificationFileWriteRepository):
    pass
