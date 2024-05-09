from ninja import UploadedFile
from pydantic import PositiveInt

from application.meta_context.domain_layer.value_object.certification.meta_certification import (
    Certification,
)


class CertificationService:
    def register_certification_files(self, certification_id: PositiveInt, files: list[UploadedFile]) -> Certification:
        certification: Certification = Certification(id=certification_id)
        certification.register_certification_files(files=files)
        return certification

    def find_by_certification_id(self, certification_id: PositiveInt) -> Certification:
        return Certification(id=certification_id)

    def delete_certification_file(self, certification_id: PositiveInt, file_id: PositiveInt) -> Certification:
        return Certification(id=certification_id).set_file_as_deleted(file_id=file_id)
