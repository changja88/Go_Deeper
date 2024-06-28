# 파이썬의 데코레이터

- PEP-318에서 기존 함수와 메서드의 기능을 쉽게 수정하기 위한 수단으로 소개되었다
- 파이썬에서 함수는 일반적인 객체일 뿐이다
    - 즉 변수에 할당하거나 파라미터로 전달하거나 다른 함수에서 다시 기존 함수를 호출하도록 할 수 있다
- `데코레이터는 데코레이터 이후에 나오는 것을 데코레이터의 첫 번째 파라미터로 하고 데코레이터의 결과 값을 반환하게 하는 문법적 설탕일 뿐이다`
- 데코레이터는 가독성을 크게 향상시킨다
    - 독자는 한 곳에서 함수의 전체 정의를 차을 수 있기 때문이다
    - 데코레이터를 적용받고 있는 함수를 "래핑된"객체라 한다

## 핰수 데코레이터

- 가장 간단한 방법은 함수에 적용하는 것이다
    - 파라미터 유효성 검사
    - 사전조건을 검사
    - 기능 전체를 새롭게 수정
    - 서명을 변경
    - 원래 함수의 결과를 캐시

```python
class ControlledException(Exception):
    """"도메인에서 발생하는 일반적인 예외"""


def retry(operation):
    @wrap(operation)
    def wrapped(*args, **kwargs):
        last_raise = None
        RETRIES_LIMIT = 3
        for _ in range(RETRIES_LIMIT):
            try:
                return operation(*args, **kwargs)
            except ControlledException as e:
                last_raise = 2
            raise last_raise
        return wrapped

```

```python
@retry
def run_operation:
    """실행중 예외가 발생할 것으로 예상되는 특정 작업을 실행"""
    return task.run()
```

- 데코레이터는 파라미터가 필요 없으므로 어떤 함수에도 쉽게 적용할 수 있다

## 클래스 데코레이터

- 클래스 데코레이터는 PEP-3129에서 도입되었으며 함수 데코레이터와 매우 유사하다. 차이점은 래퍼가 함수가 아니라 클래스라는 점이다
- 클래스 데코레이터가 복잡하고 가독성을 떨어뜨릴수 있다
    - 클래스에서 정의한 속성과 메서드를 데코레이터 안에서 완전히 다른 용도로 변경할 수 있기 때문

```python
class LoginEventSerializer:
    def __init__(self, event):
        self.event = event

    def serialize(self) -> dict:
        return {
            'usernmae': self.event..username,
            "password": "없음",
            "ip": self.event.ip,
            'timestamp': self.event.timestamp
        }


@dataclass
class LoginEvent:
    SERIALIZER = LoginEventSerializer

    username: str
    password: str
    ip: str
    timestamp: datetime

    def serialize(self) -> dict:
        return self.SERIALIZER(self).serialize()

```

- 위 방법은 처음에는 잘 동작 하지만 시간이 지나면서 시스템을 확장할수록 다음과 같은 문제가 발생한다
    - 클래스가 너무 많아 진다 : 이벤트 클래스와 직렬화 클래스가 1:1로 매핑되어 있으므로 직렬화 클래스가 점점 많아지게 된다
    - 유연하지 않다 : 만약 password를 가진 다른 클래스에서도 이 필드를 숨기려면 함수로 분리한 다음 여러 클래스에서 호출해야 한다
    - 표준화: serialize()메서드는 모든 이벤트 클래스에 있어야만 한다. 비록 믹스인을 사용해 다른 클래스로 분리할 수 있지만 상속을 제대로 했다고 볼 수 없다

```python
from datetime import datetime


def hide_field(field) -> str:
    return "**민감한 정보 삭제**"


def format_time(field_timestamp: datetime) -> str:
    return field_timestamp.strftime("%Y-%m-%d %H:%M")


def show_original(event_field):
    return event_field


class EventSerializer:
    def __init__(self, serialization_fields: dict) -> None:
        self.serialization_fields = serialization_fields

    def serialize(self, event) -> dict:
        return {
            field: transformation(getattr(event, field))
            for field, transformation
            in self.serialization_fields.items()
        }


class Serialization:
    def __init__(self, **transformations):
        self.serializer = EventSerializer(transformations)

    def __call__(self, event_class):
        def serialize_method(event_instance):
            return self.serializer.serialize(event_instance)

        event_class.serialize = serialize_method
        return event_class


@Serialization(
    username=show_original,
    password=hide_field,
    ip=show_original,
    timestamp=format_time()
)
@dataclass
class LoginEvent:
    username: str
    password: str
    ip: str
    timestamp: datetime

```

- 위 코드 처럼 이벤트 인스턴스와 변형 함수를 필터로 받아서 동적으로 객체를 만드는 것이다
    - 필터를 이벤트 인스턴스의 필드드레 적용해 직렬화하는 것이다
    - 각 필드를 변형할 함수를 만든 다음 이들을 조합해 직렬화 객체를 만들면 된다
- 데코레이터를 사용하면 다른 클래스의 코드를 확인하지 않고도 각 필드가 어떻게 처리되는지 쉽게 알 수 있다

## 다른 유형의 데코레이터

- 제너레이터나 코루틴, 심지어 이미 데코레이트된 객체도 데코레이트가 가능하다
    - 즉 데코레이터는 스택 형태로 쌓일 수 있따

# 고급 데코레이터

- 데코레이터를 사용하여 관심사를 더 작은 기능으로 분리하고 코드를 재상요할 수 있다
    - 효율적으로 사용하려면 데코레이터에 파라미터를 추가할 수 있어야 한다

## 데코레이터에 인자 전달

- 가장 일반적인 방법은 간접 참조를 통해 새로운 레벨의 중첩 함수를 만들어 데코레이터의 모든 것을 한 단게 더 깊게 만드는 것이다
    - 간접참조 : a=1; b=a; c=b 처럼 실제 값을 직접적인 경로를 통해 가져오는 것이 아니라 간접적인 경로를 거친 다음에 가져오는 것
- 두번째 방법은 데코레이터를 위한 클래스를 만드는 것이다
    - 세 단계 이상 중첩된 클로저 함수보다 이해하기 쉽기 떄문에 가독성이 좋다

### 중첩 함수를 사용한 데코레이터

- 데코레이터에 파라미터를 추가하려면 다른 수준의 간접 참조가 필요한다
    - 첫 번째 함수는 파라미터를 받아서 내부 함수에 전달한다
    - 두 번째 함수는 데코레이터가 될 함수다
    - 세 번째 함수는 데코레이팅의 결과를 반환하는 함수다
    - 즉, 최소 세 단계의 중첩 함수가 필요하다

```python
_DEFAULT_RETRIES_LIMIT = 3


def with_retry(
        retries_limit: int = _DEFAULT_RETRIES_LIMIT,
        allowed_exceptions: Optional[Sequence[Exception]] = None,
):
    allowed_exceptions = allowed_exceptions or (ControlledException,)

    def retry(operation):

        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(retries_limit):
                try:
                    return operation(*args, **kwargs)
                except allowed_exceptions as e:
                    logger.warning(
                        "%s 재시도, 원인: %s",
                        operation.__qualname__, e
                    )
                    last_raised = e
            raise last_raised

        return wrapped

    return retry


@with_retry()
def run_operation(task):
    return task.run()


@with_retry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()


@with_retry(allowed_exceptions=(AttributeError,))
def run_with_custom_exceptions(task):
    return task.run()


@with_retry(
    retries_limit=4, allowed_exceptions=(ZeroDivisionError, AttributeError)
)
def run_with_custom_parameters(task):
    return task.run()
```

- 위 코드는 의미상 아래 코드와 같다
    - <original_function> = retry(arg1, arg2, ...)(<original_function)
- 위 방법은 대부분의 경우에 잘 작동하지만, 새로운 함수가 추가될 때마다 들여쓰기가 추가되어 너무 많은 충접 함수가 필요하다
    - 또한 함수는 상태를 저장하지 않기 때문에 객체가 하는 것처럼 내부 데이터를 관리하기가 어렵다

### 데코레이터 객체

- 위 예제에서는 세 단계의 중첩 함수가 필요하다
- 클래스를 사용하면 깔끔하게 데이코레이터를 정의할 수 있다
    - __init__ 메서드에 파라미터를 전달한 다음 __call__이라는 매직 메서드에서 데코레이터의 로직을 구현하면 된다

```python
class WithRetry:
    def __init__(
            self,
            retries_limit: int = _DEFAULT_RETRIES_LIMIT,
            allowed_exceptions: Optional[Sequence[Exception]] = None,
    ) -> None:
        self.retries_limit = retries_limit
        self.allowed_exceptions = allowed_exceptions or (ControlledException,)

    def __call__(self, operation):
        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(self.retries_limit):
                try:
                    return operation(*args, **kwargs)
                except self.allowed_exceptions as e:
                    logger.warning(
                        "%s 재시도, 원인: %s",
                        operation.__qualname__, e
                    )
                    last_raised = e
            raise last_raised

        return wrapped

@with_retry(retries_limit=5)
def run_with_custom_retries_limit(task):
  return task.run()

```

## 기본값을 가진 데코레이터

- 파이썬 구문이 어떻게 처리되는지 이해하는 것이 중요하다
    - 먼저 @연산 전에 전달된 파라미터를 사용해 데코레이터 객체를 생성한다
    - 데코레이터 객체는 __init__메서드에서 정해진 로직에 따라 초기화를 진행한다
    - 그 다음 @ 연산이 호출된다
    - 데코레이터 객체는 run_with_custom_retries_limit함수를 래핑하여 __call__매직 메서드를 호출한다
    - __cal__ 매직 메서드는 앞의 데코레이터에서 하던 것 처럼 원본 함수를 래핑하여 원하는 로직이 적용된 새로운 함수를 반환한다 