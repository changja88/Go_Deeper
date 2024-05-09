from enum import StrEnum, auto, unique

from application.meta_context.domain_layer.meta_enum import FinanceMetaType

BACKGROUND_EVALUATION_TYPE_SOURCE_SET: set[FinanceMetaType] = {
    FinanceMetaType.FAMILY_ASSET,
    FinanceMetaType.FATHER_JOB,
    FinanceMetaType.MOTHER_JOB,
}

ASSET_EVALUATION_TYPE_SOURCE_SET: set[FinanceMetaType] = {FinanceMetaType.ASSET, FinanceMetaType.CAR_PRICE}
WORK_EVALUATION_TYPE_SOURCE_SET: set[FinanceMetaType] = {FinanceMetaType.JOB, FinanceMetaType.COMPANY}


@unique
class EvaluationType(StrEnum):
    INCOME = auto()
    WORK = auto()
    ASSET = auto()
    EDUCATION = auto()
    APPEARANCE = auto()
    BIRTH_YEAR = auto()
    BACKGROUND = auto()


@unique
class EvaluationSourceType(StrEnum):
    JOB_SOURCE = auto()
    INCOME_SOURCE = auto()
    COMPANY_SOURCE = auto()
    ASSET_SOURCE = auto()
    CAR_PRICE_SOURCE = auto()
    FAMILY_ASSET_SOURCE = auto()
    MOTHER_JOB_SOURCE = auto()
    FATHER_JOB_SOURCE = auto()
    EDUCATION_SOURCE = auto()
    APPEARANCE_SOURCE = auto()
    BIRTH_YEAR_SOURCE = auto()
