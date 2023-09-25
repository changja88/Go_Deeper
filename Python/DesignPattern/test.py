from typing import Any, Literal


def validate_simple(data: Any) -> True:  # 항상 True를 반환합니다
    return False


MODE = Literal['r', 'rb', 'w', 'wb']


def open_helper(file: str, mode: MODE) -> str:
    ...


open_helper('/some/path', 'r')  # 형 검사기를 통과합니다
open_helper('/other/path', 'type')  # 형 검사기에서 에러입니다


