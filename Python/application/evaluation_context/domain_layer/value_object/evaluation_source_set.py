from pydantic import Field
from pydantic.json_schema import SkipJsonSchema

from applications.common.enum import Gender
from applications.common.ninja.custom_entity_model import ValueObject
from application.evaluation_context.domain_layer.evaluation_enum import (
    EvaluationSourceType,
)
from application.evaluation_context.domain_layer.value_object.evaluation_source import (
    EvaluationSource,
)
from application.evaluation_context.infra_layer.repository.evaluation_source_repositories import (
    EvaluationSourceCompoundRepository,
)


class EvaluationSourceSet(ValueObject):

    job_source: EvaluationSource = Field(default=0)
    income_source: EvaluationSource = Field(default=0)
    company_source: EvaluationSource = Field(default=0)
    asset_source: EvaluationSource = Field(default=0)
    car_price_source_: EvaluationSource = Field(default=0)
    family_asset_source: EvaluationSource = Field(default=0)
    mother_job_source: EvaluationSource = Field(default=0)
    father_job_source: EvaluationSource = Field(default=0)
    appearance_source: EvaluationSource = Field(default=0)
    education_source: EvaluationSource = Field(default=0)
    birth_year_source: EvaluationSource = Field(default=0)
    repo: SkipJsonSchema[EvaluationSourceCompoundRepository] = Field(exclude=True)

    def __init__(self, gender: Gender, repo: EvaluationSourceCompoundRepository = EvaluationSourceCompoundRepository()):
        super().__init__(
            job_source=repo.find_evaluation_source_by(EvaluationSourceType.JOB_SOURCE, gender),
            income_source=repo.find_evaluation_source_by(EvaluationSourceType.INCOME_SOURCE, gender),
            company_source=repo.find_evaluation_source_by(EvaluationSourceType.COMPANY_SOURCE, gender),
            asset_source=repo.find_evaluation_source_by(EvaluationSourceType.ASSET_SOURCE, gender),
            car_price_source=repo.find_evaluation_source_by(EvaluationSourceType.CAR_PRICE_SOURCE, gender),
            family_asset_source=repo.find_evaluation_source_by(EvaluationSourceType.FAMILY_ASSET_SOURCE, gender),
            mother_job_source=repo.find_evaluation_source_by(EvaluationSourceType.MOTHER_JOB_SOURCE, gender),
            father_job_source=repo.find_evaluation_source_by(EvaluationSourceType.FATHER_JOB_SOURCE, gender),
            appearance_source=repo.find_evaluation_source_by(EvaluationSourceType.APPEARANCE_SOURCE, gender),
            birth_year_source=repo.find_evaluation_source_by(EvaluationSourceType.BIRTH_YEAR_SOURCE, gender),
            education_source=repo.find_evaluation_source_by(EvaluationSourceType.EDUCATION_SOURCE, gender),
            repo=repo,
        )
