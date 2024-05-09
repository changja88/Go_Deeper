from enum import StrEnum, auto, unique

IDEAL_EVALUATION_POINT_RANGE_PERCENTAGE = 2


@unique
class MatchingStatus(StrEnum):
    PENDING = auto()
    REJECTED = auto()
    APPROVED = auto()
