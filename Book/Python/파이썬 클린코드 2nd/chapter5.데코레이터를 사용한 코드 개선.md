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

- 파이썬 구문이 어떻게 처리되는지 이해하는 것이 중요하다
    - 먼저 @연산 전에 전달된 파라미터를 사용해 데코레이터 객체를 생성한다
    - 데코레이터 객체는 __init__메서드에서 정해진 로직에 따라 초기화를 진행한다
    - 그 다음 @ 연산이 호출된다
    - 데코레이터 객체는 run_with_custom_retries_limit함수를 래핑하여 __call__매직 메서드를 호출한다
    - __cal__ 매직 메서드는 앞의 데코레이터에서 하던 것 처럼 원본 함수를 래핑하여 원하는 로직이 적용된 새로운 함수를 반환한다

## 기본값을 가진 데코레이터

```python
@retry()
def my_function():
    ...


@retry
def my_function():
    ...
```

- 위 두 코드에는 차이가 있다
    - 괄호가 없는 경우에는 첫 번째 파라미터로 함수가 전달되지만, 괄호가 있는 경우에는 첫 번째 파라미터로 None이 전달된다
    - 문서를 확인하면 첫번째 방식이 올바른 방식이다. 두 번째 방식은 호출 시 에러가 발생하기 때문에 주의해서 사용해야 한다
- 위 두가지 방식을 모두 지원하려면 추가적인 작업이 필요하다

```python
@decorator(x=3, y=4)
def my_function(x, y):
    return x + y


my_function()  # 7


def decorator(function=None, *, x=DEFAULT_X, y=DEFAULT_Y):
    if function is None:
        # @decorator(...) 형태로 괄호를 사용해서 호출한 경우
        def decorated(function):
            @wraps(function)
            def wrapped():
                return function(x, y)

            return wrapped

        return decorated
    else:
        # @decorator 형태로 괄호가 없이 호출한 경우
        @wraps(function)
        def wrapped():
            return function(x, y)

        return wrapped
```

- 데코레이터에 기본값이 있기 때문에 함수의 인지가 없이도 호출할 수 있다
- 위 코드에서 주의할 것은 파라미터가 키워드 전용이다
    - 이렇게 함으로써 데이코레이터의 서명이 간단해졌다
    - 이렇게 하면 괄호를 사용하여 x,y를 전달하는 경우 function파라미터의 값은 None이 될 것이기 떄문이다
    - 위치 기반으로 파라미터를 넘기면 첫 번째 인자가 무엇인지 헷갈릴 것이다

```python
def decorator(function=None, *, x=DEFAULT_X, y=DEFAULT_Y):
    if function is None:
        return lambda f: decorator(f, x=x, y=y)

    @wraps(function)
    def warapped():
        return function(x, y)

    return warapped
```

- 또 다른 방법은 래핑된 데코레이터의 일부를 추상화한 다음 함수의 일부에 적용하는 것이다
    - 이를 위해 중간 상태를 취하고 람다 함수를 사용하였다

## 데코레이터를 위한 확장 구문

```python
def _log(f, *args, **kwargs):
    print(f"함수 이름: {f.__qualname__!r}, 파라미터: {args=}와 {kwargs=}")
    return f(*args, **kwargs)


@(lambda f: lambda *args, **kwargs: _log(f, *args, **kwargs))
def func(x):
    return x + 1
```

- PEP-614 에서 보다 일반화된 문법을 지원하는 새로운 데코렝이터 문법이 추가되었다
    - 이전에는 @를 사용할 수 있는 범위가 제한적이어서 모든 함수 표현식에 적용할 수 없었다
    - 이제 이러한 제약이 해제되어 보다 복잡한 표현식을 데코레이터에 사용할 수 있게 되었다
    - 하지만 너무 복잡한 기능을 축약하여 가독성을 떨어뜨리지 않도록 주의 해야한다
- 위 구문은 아래의 경우에 유용하게 쓰일수 있다
    - 표현식을 평가 하기 위해 no-op을 단순화한다거나 eval함수를 호출하지 않도록 하는 것이다

# 데코레이터의 활용 - 흔한 실수 피하기

## 래핑된 원본 객체의 데이터 보존

- 가장 많이 실수 하는 것 중에 하나는 우너본 함수의 일부를 프로퍼티나 또는 속성을 유지하지 않아 원하는 않는 부작용을 유발한다는 것이다

```python
def trace_decorator(function):
    def wrapped(*args, **kwargs):
        logger.info('')
        return function(*args, **kwargs)

    return wrapped


@trace_decorator
def process_account(account_id: str):
    pass
```

- 원본 함수의 정의와 비교해 함수가 전혀 수정되지 않은 것처럼 보일 것이다
    - 하지만 원래 데코레이터는 기존 함수의 어떤 것도 변경하지 않아야 하지만 이번 코드는 어떤 결함으로 인해 함수명과 docstring을 변경해버렸다
    - help(process_account)
    - 데코레이터 원본 함수를 wrapped라 불리우는 새로운 함수로 변경해버렸기 때문에 원본 함수의 속성이 아닌 새로운 함수의 속성을 출력하고 있는 것이다

```python
def trace_decorator(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        logger.info('')
        return function(*args, **kwargs)

    return wrapped
```

- 위 처럼 코드를 수정하면 해결된다
    - @warps데코레이터를 적용하여 실제로는 function파리미터 함수를 래핑한 것이라고 알려주는 것이다
    - 위와 같은 형태가 가장 일반적인 데코레이터 포맷이다

## 데코레이터 부작용 처리

- 데코레이터 함수를 구현할 때 지켜야할 단 하나의 조건은 구현 함수 가장 안쪽에 위치해야 한다는 것이다
    - 그렇게 하지 않으면 임포팅과 관련된 문제가 발생할 수 있다
    - 그럼에도 불구하고 떄로는 이러한 부작용이 필요한(심지어 바람직한)경우도 있고, 반대의 경우도 있따

### 데코레이터 부작용의 잘못된 처리

```python
def traced_function_wrong(function):
    logger.info("%s 함수 실행", function)
    start_time = time.time()

    @wraps(function)
    def wrapped(*args, **kwargs):
        result = function(*args, **kwargs)
        logger.info(
            "함수 종료 시간: %.2fs", function, time.time() - start_time
        )
        return result

    return wrapped


@traced_function_wrong
def process_with_delay(callback, delay=0):
    time.sleep(delay)
    return callback()
```

- 위 코드는 잘 동작할것 같지만 그렇지 않다
    - 문제는 함수를 임포트만 하여도 데코레이터 함수가 실행되고 있다
    - process_with_delay = traced_function_wrong(prcess_with_delay)
    - 위 문장은 모듈을 임포트할 때 실행된다. 따라서 함수에 설정된 start_time은 모듈을 처음 임포트할 때의 시간이 된다
    - 함수를 연속적으로 호출하면 함수의 실행시간으로 최초 시작 시점과의 시간차를 계산한다 -> 잘못된 값

```python
def traced_function(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        logger.info("%s 함수 실행", function.__qualname__)
        start_time = time.time()
        result = function(*args, **kwargs)
        logger.info(
            "함수 %s의 실행시간: %.2fs",
            function.__qualname__,
            time.time() - start_time
        )
        return result

    return wrapped
```

- 위 코드 처럼 수정하여 해결할 수 있다
    - 실행을 지연시키기 위해 래핑된 함수 내부로 코드를 이동시키기만 하면된다

## 데코레이터 부작용의 활용

- 때로는 부작용을 의도적으로 사용하여 실제 실행이 가능한 시점까지 기다리지 않는 경우도 있다
    - 대표적인 예로 모듈의 공용 레지스트리에 객체를 등록하는 경우가 있다
    - 예를 들어 이전 이벤트 시스템에서 일부 이벤트만 사용하려는 경우를 살펴보자
    - 이런 경우 이벤트 계층 구조 중간에 가상의 클래스를 만들고 일부 파생 클래스에 대해서만 이벤트를 처리하도록 할 수 있다
    - 각 클래스마다 처리 여부를 플래그로 표시하는 대신 데코레이터를 사용해 명시적으로 레지스트리에 등록할 수 있다

```python
EVENTS_REGISTRY = {}


def register_event(event_cls):
    EVENTS_REGISTRY[event_cls.__name__] = event_cls
    return event_cls


class Event:
    """기본 이벤트 객체"""


class UserEvent:
    TYPE = "user"


@register_event
class UserLoginEvent(UserEvent):
    """사용자가 시스템에 접근했을 때 발생하는 이벤트"""


@register_event
class UserLogoutEvent(UserEvent):
    """사용자가 시스템에서 나갈 때 발생하는 이벤트"""
```

- 위 코드에서 처음에는 EVENTS_REGISTRY는 비어 있는 것처럼 보이지만 이 모듈의 일부를 임포트 하면 register_event 데코레이터로 지정한 클래스로 채워지게 된다
    - 이런 동작 방식이 문제가 되는 경우도 있지만 어떤 경우에는 이 패턴이 필요하 ㄴ경우가 있다
    - 사실 많은 웹 프레임워크나 널리 알려진 라이브러리들은 이 원리로 객체를 노출하거나 활용하고 있다

## 어느 곳에서나 동작하는 데코레이터 만들기

- *args, **kwargs 서명을 사용하여 데코레이터를 정의하면 모든 경우에 사용할 수 있다
    - 그러나 다음 두 가지 이유로 원래 서명과 비슷하게 데코레이터를 정의하는 것이 좋을 떄가 있다
    - 1> 원래 함수와 모양이 비슷하기 때문에 읽기가 쉽다
    - 2> 파라미터를 받아서 뭔가를 하려면 *args, **kwargs를 사용하는 것이 불편하다

```python
# src/decorator_universal_1.py
from functools import wraps
from log import logger


class DBDriver:
    def __init__(self, dbstring: str) -> None:
        self.dbstring = dbstring

    def execute(self, query: str) -> str:
        return f"query {query} at {self.dbstring}"


def inject_db_driver(function):
    @wraps(function)
    def wrapped(dbstring):
        return function(DBDriver(dbstring))

    return wrapped


@inject_db_driver
def run_query(driver):
    return driver.execute("test_function")


run_query("test_OK")
```

- DBDriver 객체는 연결 문자열을 받아서 데이터베이스에 연결하고 DB 연산을 수행하는 객체이다
    - 메서드는 DB 정보 문자열을 받아서 DBDrivver 인스턴스를 생성한다
    - 데코레이터는 이러한 변환을 자동화하여 문자열을 받아 DBDriver를 생성하고 함수에 전달한다
    - 따라서 마치 객체를 직접 받은 것처럼 가정할 수 있다
- 하지만 이제 같은 기능을 하는 데코레이터를 클래스 메서드에서 재사용하려고 싶다면 어떻게 해야 할까?

```python
class DataHandler:
    @inject_db_driver
    def run_query(self, driver):
        return driver.execute(self.__class__.__name__)


DataHandler().run_query('test_fails')
```

- 위 코드처럼 실행하면 동작하지 않는다
    - 클래스의 메서드에는 self라는 추가 변수가 있다
    - 따라서 하나의 파라미터만 받도록 설계된 이 데코레이터는 연결 문자열 자리에 self를 전달하고, 두 번째 파라미터에는 아무것도 전달하지 않아서 에러가 발생한다
    - 이 문제를 해결하려면 메서드와 함수에 대해서 동일하게 동작하는 데코레이터를 만들어야 한다
    - 즉, 디스크립터 프로토콜을 구현한 데코레이터 객체를 만들어야 한다

```python
class inject_db_driver:
    """문자열을 DBDriver 인스턴스로 변환하여 래핑된 함수에 전달"""

    def __init__(self, function) -> None:
        self.function = function
        wraps(self.function)(self)

    def __call__(self, dbstring):
        return self.function(DBDriver(dbstring))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.__class__(MethodType(self.function, instance))
```

- 호출할 수 있는 객체를 메서드에 다시 바인딩한다는 점이 중요하다
    - 즉, 함수를 개체에 바인딩하고 데코레이터를 새로운 호출 가능 객체로 다시 생성한다
    - 함수의 경우 __get__메서드를 사용하지 않기 때문에 여전히 잘 작동한다

# 데코레이터와 클린 코드

## 상속보다 컴포지션(composition)

- 일반적으로 상속보다는 컴포지션이 더 좋은 선택이다
    - 왜냐하면 상속은 코드의 결합도를 높게 만들어서 몇 가지 문제를 수반하기 때문이다

```python
class BaseResolverMixin:
    def __getattr__(self, attr: str):
        if attr.startswith("resolve_"):
            _, actual_attr = attr.partition("resolve_")
        else:
            actual_attr = attr
        try:
            return self.__dict__[actual_attr]
        except KeyError as e:
            raise AttributeError from e


@dataclass
class Customer(BaseResolverMixin):
    customer_id: str
    name: str
    address: str
```

- 위 코드는 x라는 변수에 대해서 resolve_x를 만드는 것처럼 일일이 모든 변수에 대해서 resolve_를 붙여준다
    - __getattr__ 매직 메서드를 통해서 이를 구현 했다
    - 상속도 사용했다

```python
from dataclasses import dataclass


def _resolver_method(self, attr):
    if attr.startswith("resolve_"):
        _, actual_attr = attr.partition("resolve_")
    else:
        actual_attr = attr
    try:
        return self.__dict__[actual_attr]
    except KeyError as e:
        raise AttributeError from e


def with_resolver(cls):
    cls.__getattr__ = _resolver_method
    return cls


@dataclass
@with_resolver
class Customer:
    customer_id: str
    name: str
    address: str


customer = Customer("1", "name", "address")
customer.resolve_customer_id
customer.resolve_name
```

- 위 코드처럼 데코레이터를 만들어 볼 수 있다
- __getattr__과 유사한 서명을 가진 독립 함수를 결정(resovle)메서드 _resolver_method로 만들었다
    - 그래서 _resolver_method의 첫 번째 파라미터도 의도적으로 self로 사용하여 원래의 __getattr__메서드가 함수로 변경되었음을 표시했다
- 데코레이터를 사용한 방식이 이전 방식보다 나은 점은 무서을까?
    - 우선 상속대신 컴포지션을 사용하고 있음을 의미한다 -> 기본 클래스와 덜 결합되어 있다
    - 상속을 사용하는 것은 현실적이지 않다 -> getattr메서드를 활용하기 위해 더 전문화된 상속을 사용하지는 않는다
    - 상속에서는 is-a 관계가 성립되지 않는다

## 데코레이터와 DRY 원칙

- 재사용을 위해 데코레이터를 사용할 때 염두에 두어야 할 것이 있다
    - 실질적으로 코드 사용량을 줄일 수 있다는 확실한 믿음이 있어야 한다
    - 모든 데코레이터, 특히 신중하게 설계되지 않은 데코레이터는 코드의 복잡성을 증가시킨다
    - 그다지 재사용할 필요가 없을 경우 별개의 함수나 작은 클래스로도 충분한 경우가 있다
- 기존 코드를 데코레이터로 리팩토링할지 결정하는 기준은 무엇일까?
    - 파이썬의 데코레이터에 적용되는 특별한 기준은 없지만, 소프트웨어 공학에서 일반적으로 적용되는 원칙(GLASS 01)을 따를 수 있다
    - 컴포넌트가 충분히 재사용 가능한 추상화를 했다고 인정받기 위해서는 적어도 3가지 이상의 애플리케이션에서 시험해봐야 한다는 것이다
    - 또한 레퍼런스에서 재사용 가능한 컴포넌트를 만드는 것은 일반 컴포넌트를 만드는 것보다 세배나 더 어렵다는 내용이 있다
- 1> 처음부터 데코레이터를 만들지 않는다. 패턴이 생기고 ㄷ에코레이터에 대한 추상화가 명확해지면 그 떄 맆팩토링을 한다
- 2> 데코레이터가 적어도 3회 이상 필요한 경우에만 궇현한다
- 3> 데코레이터 코드를 최소한으로 유지한다

## 데코레이터와 관심사의 분리

- 코드 재사용의 핵심은 응집력이 있는 컴포넌트를 만드는 것이다
    - 즉, 최소한의 책임을 가져서 오직 한 가지 일만 해야 하며, 그 일을 잘 해야 한다
    - 컴포넌트가 작을 수록 재사용성이 높아진다

```python
def traced_function(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        logger.info("%s 함수 실행", function.__qualname__)
        start_time = time.time()
        result = function(*args, **kwargs)
        logger.info(
            "함수 %s의 실행시간: %.2fs",
            function.__qualname__,
            time.time() - start_time
        )
        return result

    return wrapped
```

- 위 코드는 특정 함수의 실행을 추적하는 데코레이터이다
    - 이 데코레이터는 동작에 문제가 있다
    - 하나 이상의 작업을 수행하고 있다

```python
def log_execution(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        logger.info("%s 함수 실행", function.__qualname__)
        return function(*args, **kwargs)

    return wrapped


def measure_time(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = function(*args, **kwargs)
        logger.info(
            "함수 %s의 실행시간: %.2fs",
            function.__qualname__,
            time.time() - start_time
        )
        return result

    return wrapped


@measure_time
@log_execution
def operation():
    ...
```

- 위 코드처럼 제한적인 책임을 지닌 더 작은 데코레이터로 분류되어야 한다

# 좋은 데코레이터 분석

- 좋은 데코레이터가 갖추어야 할 특성은 다음과 같다
    - 1> 캡슐화와 관심사의 분리 : 좋은 데코레이터는 실제로 하는 일과 데코레이팅하는 일의 책임을 명확히 구분해야 한다. 어설프게 추상화를 하면 안된다. 즉 데코레이터의 클라이언트는 내부에서 어떻게 수현했는지
      전혀 알 수 없는 블랙박스 모드로 동작해야 한다 
    - 2> 독립성 : 데코레이터가 하는 일은 독립적이어야 하며 데코레이팅되는 객체와 최대한 분리되어야 한다
    - 3> 재사용성 : 데코레이터는 하나의 함수 인스턴스에만 적용되는 것이 아니라 여러 유형에 적용 가능한 형태가 바람직하다. 왜냐하면 하나의 함수에만 적용된다면 데코레이터가 아니라 함수로 대신할 수도 있기 때문이다. 즉 충분히 범용적이어야 한다
    - 