from pydantic import PositiveInt

from applications.common.ninja.custom_entity_model import ValueObject


class Question(ValueObject):
    id: int
    type: str
    question: str
    order: int


class Answer(ValueObject):
    id: int
    order: int
    answer: str


class Problem(ValueObject):
    question: Question
    answers: list[Answer]

    def get_answer_count_of(self) -> PositiveInt:
        # 해당 문제의 선택지의 갯수 (ex.3번 문제는 4개의 선택지가 있다)
        return len(self.answers)


class DateTest(ValueObject):
    problems: list[Problem]


class ProblemResponse(ValueObject):
    question: Question
    answer: Answer
