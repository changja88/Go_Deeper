from typing import Optional, Self

from django.core.files.uploadedfile import UploadedFile
from pydantic import Field, PositiveInt
from pydantic.json_schema import SkipJsonSchema

from applications.common.ninja.custom_entity_model import ValueObject
from application.meta_context.domain_layer.meta_enum import CensorStatus
from application.meta_context.domain_layer.value_object.file import CertificationFile
from application.meta_context.infra_layer.repository.certification_file_repositories import (
    CertificationFileCompoundRepository,
)
from application.meta_context.infra_layer.repository.certification_repositories import (
    CertificationCompoundRepository,
)


class Certification(ValueObject):
    id: PositiveInt
    rejected_reason: Optional[str] = Field(default=None)
    censor_status: CensorStatus = Field(default=CensorStatus.UNDER_CENSOR)
    certification_files: list[CertificationFile] = Field(default_factory=list)
    certification_repo: SkipJsonSchema[CertificationCompoundRepository] = Field(exclude=True)
    file_repo: SkipJsonSchema[CertificationFileCompoundRepository] = Field(exclude=True)

    def __init__(
        self,
        id: PositiveInt,
        certification_repo: CertificationCompoundRepository = CertificationCompoundRepository(),
        file_repo: CertificationFileCompoundRepository = CertificationFileCompoundRepository(),
    ):
        rejected_reason, censor_status = certification_repo.find_rejected_reason_and_censor_status(id)
        super().__init__(
            id=id,
            rejected_reason=rejected_reason,
            censor_status=censor_status,
            certification_files=file_repo.find_all_by_id(certification_id=id),
            certification_repo=certification_repo,
            file_repo=file_repo,
        )

    def register_certification_files(self, files: list[UploadedFile]) -> Self:
        self.certification_files = self.file_repo.register_certification_files(certification_id=self.id, files=files)
        return self

    def set_file_as_deleted(self, file_id: PositiveInt) -> Self:
        for file in self.certification_files:
            if file.id == file_id:
                self.certification_files.remove(file)
                self.file_repo.set_file_as_deleted(file_id=file.id)
        return self
