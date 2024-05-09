from pydantic import Field, NonNegativeInt

from application.evaluation_context.domain_layer.evaluation_enum import EvaluationType

WANTED_WEIGHT_TYPE = EvaluationType


WANTED_POINT_CUT_OFF_PERCENTAGE = 10  # 원티드 포인트 구성에 사용할 수 있는 포인트
AVAILABLE_WANTED_WEIGHT_POINT_TOTAL: NonNegativeInt = Field(
    default=len(WANTED_WEIGHT_TYPE) * WANTED_POINT_CUT_OFF_PERCENTAGE, exclude=True
)
"""
UI상 1점씩 움직일 수 있고 부여 포인트는 50점
- 조절 가능 항목이 7개 이고 멤버의 10%를 조정 할 수 있기 때문에 (100(항목만점) * 10%) * 7개 = 70
"""
