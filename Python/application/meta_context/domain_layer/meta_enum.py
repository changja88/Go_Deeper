from enum import StrEnum, auto, unique


class MetaType(StrEnum): ...


@unique
class PhotoType(MetaType):
    FACE = auto()
    ETC = auto()


@unique
class PhysicalMetaType(MetaType):
    BODY_SHAPE = auto()
    HEIGHT = auto()
    WEIGHT = auto()


@unique
class FinanceMetaType(MetaType):
    INCOME = auto()
    JOB = auto()
    COMPANY = auto()
    ASSET = auto()
    CAR_BRAND = auto()
    CAR_PRICE = auto()
    FAMILY_ASSET = auto()
    MOTHER_JOB = auto()
    FATHER_JOB = auto()


@unique
class UniversityType(MetaType):
    DOMESTIC = auto()
    INTERNATIONAL = auto()


@unique
class PreferenceMetaType(MetaType):
    SMOKING = auto()
    ALCOHOL = auto()
    HOBBY = auto()
    RELIGION = auto()
    DATE_STYLE = auto()
    MBTI = auto()
    KEYWORD = auto()
    GROWTH = auto()


SINGLE_SELECTION_PREFERENCE_META: set[PreferenceMetaType] = {
    PreferenceMetaType.SMOKING,
    PreferenceMetaType.ALCOHOL,
    PreferenceMetaType.RELIGION,
    PreferenceMetaType.MBTI,
}
MULTI_SELECTION_PREFERENCE_META: set[PreferenceMetaType] = {
    PreferenceMetaType.HOBBY,
    PreferenceMetaType.DATE_STYLE,
    PreferenceMetaType.KEYWORD,
    PreferenceMetaType.GROWTH,
}


@unique
class CensorStatus(StrEnum):
    UNDER_CENSOR = auto()
    APPROVED = auto()
    REJECTED = auto()
