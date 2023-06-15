## [파이썬 typing 모듈](https://python.flowdas.com/library/typing.html#)

- 이 모듈은 PEP 484, PEP 526, PEP 544, PEP 586, PEP 589 및 PEP 591로 지정된 형 힌트에 대한 런타임 지원을 제공합니다. 가장 기본적인 지원은 형 Any, Union,
  Tuple, Callable, TypeVar 및 Generic으로 구성된다. 형 힌트에 대한 간략한 소개는 PEP 483을 참조하십시오.

### 형 에일리어스

- 형 엘리이어스는 별칭에 형을 대입하여 정의된다

```python
Vector = list[float]


def scale(scalar: float, vector: Vector) -> Vector:
    return [scalar * num for num in vector]


# 형 검사 통과; float의 리스트는 Vector로 적합합니다.
new_vector = scale(2.0, [1.0, -4.2, 5.4])
```

- 형 에일리어스는 복잡한 형 서명을 단순화하는데 유용하다
- 형 힌트로서의 None은 특별한 경우이며 type(None)으로 치환됨에 유의해야 한다

```python
from collections.abc import Sequence

ConnectionOptions = dict[str, str]
Address = tuple[str, int]
Server = tuple[Address, ConnectionOptions]


def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    ...


# 정적 형 검사기는 이전 형 서명을 이것과 정확히 동등한 것으로 취급합니다.
def broadcast_message(
        message: str,
        servers: Sequence[tuple[tuple[str, int], dict[str, str]]]
) -> None:
    ...

```

### NewType

- NewType() 도우미 함수를 사용하여 다른 형을 만들 수 있다

```python
from typing import NewType

UserId = NewType('UserId', int)
some_id = UserId(524313)
```

- 정적 형 검사기는 새 형을 원래 형의 서브 클래스인 것처럼 다루며 논리 에러를 잡는데 유용하다

```python
def get_user_name(user_id: UserId) -> str:
    ...


# 형 검사 통과
user_a = get_user_name(UserId(42351))
# 형 검사 실패; int는 UserId가 아닙니다
user_b = get_user_name(-1)
```

- UserId형의 변수에 대해 모든 int 연산을 여전히 수행할 수 있지만, 결과는 항상 int형이 된다 . 이것은 int가 기대되는 모든 곳에 UserId를 전달 할 수 있지만, 잘못된 방식으로 의도하지 않게
  UserId를 만들지 않도록 한다

```python
# 'output'은 형 'int'입니다, 'UserId'가 아닙니다
output = UserId(23413) + UserId(54341)
```

- 이러한 검사는 정적 형 검사기에서만 적용된다. 실행 시간에 문장 Derived = NewType('Derived', Base)는 Derived를 전달하는 매개 변수를 즉시 반환하는 함수로 만든다. 이것은
  Derived(some_value)표현식이 새로운 클래스를 만들거나 일반 함수 호출을 넘어서는 오버헤드를 발생시키지 않음을 의미한다. 더욱 정확하게, 표현식 some_value is Derived(
  some_value)는 실행 시간에 항상 참이다. 이것은 또한 Derived의 서브 형을 만들 수 없다는 것을 의미하는데, 실행 시간에 항등함수(indentity function)일 뿐 실제 형이 아니기 때문이다

```python
from typing import NewType

UserId = NewType('UserId', int)


# 실행 시간에 실패하고 형 검사를 통과하지 못합니다
class AdminUserId(UserId): pass
```

- 그러나 '파생된' NewType을 기반으로 NewType()을 만들 수 있다. 그리고 ProUserId에 대한 형 검사는 예상대로 작동한다

```python
from typing import NewType

UserId = NewType('UserId', int)

ProUserId = NewType('ProUserId', UserId)
```

### 형 에일리어스 / NewType

- 에일리어스를 사용하면 두 형이 서로 동등한 것으로 선언된다 Alias=Original이다. 모든 경우 정적 형 검사기가 Alias를 Original과 정확히 동등한 것으로
  취급하며, `복잡한 형 서명을 단순화하려는 경우에 유용하다`
- NewType은 한 형을 다른 형의 서브 형으로 선언한다. Derived = NewType('Derived', Original)은 정적 형 검사기가 Derived를 Original의 서브 클래스로 취급하게 한다.
  이는 Original형의 값이 Derived형의 값이 예상되는 위치에서 사용될 수 없음을 의미한다.` 실행 시간 비용을 최소화하면서 논리 에러를 방지하려는 경우에 유용하다`

### Callable

- 특정 서명의 콜백 함수를 기대하는 프레임워크는 Callable[[Arg1Type, Arg2Type], ReturnType]을 사용하여 형 힌트를 제공할 수 있다
- 형 힌트에서 인자 리스트를 리터럴 줄임표로 대체하여 호출 서명을 지정하지 않고 콜러블의 반환값을 선언할 수 있다 : Callable[..., ReturnType]

```python
from collections.abc import Callable


def feeder(get_next_item: Callable[[], str]) -> None:
    pass


def async_query(on_success: Callable[[int], None], on_error: Callable[[int, Exception], None]) -> None:
    pass
```

### 제네릭

- 컨네이너에 보관된 객체에 대한 형 정보는 일반적인 방식으로 정적으로 유추될 수 없기 때문에, 컨테이너 요소에 대해 기대되는 형을 나타내는 서명을 지원하도록 추상 베이스 클래스가 확장되었다

```python
from collections.abc import Mapping, Sequence


def notify_by_email(employees: Sequence[Employee],
                    overrides: Mapping[str, str]) -> None: ...
```

- 제네릭은 TypeVar라는 typing에서 제공되는 새로운 팩토리를 사용하여 매개 변수화될 수 있다

```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar('T')  # 형 변수를 선언합니다


def first(l: Sequence[T]) -> T:  # 제네릭 함수
    return l[0]
```

### 사용자 정의 제네릭 형

- 사용자 정의 클래스는 제네릭 클래스로 정의 할 수 있다

```python
from typing import TypeVar, Generic
from logging import Logger

T = TypeVar('T')


class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('%s: %s', self.name, message)
```

- 사용자 정의 제네릭 형 에일리어스도 지원한다

```python
from collections.abc import Iterable
from typing import TypeVar, Union

S = TypeVar('S')
Response = Union[Iterable[S], int]


# 여기서 반환형은 Union[Iterable[str], int]와 같습니다
def response(query: str) -> Response[str]:
    ...


T = TypeVar('T', int, float, complex)
Vec = Iterable[tuple[T, T]]


def inproduct(v: Vec[T]) -> T:  # Iterable[tuple[T, T]]와 같습니다
    return sum(x * y for x, y in v)
```

### Any 형

- 특수한 종류의 형으로 Any가 있다. 정적형 검사기는 모든 형을 Any와 호환되는 것으로, Any를 모든 형과 호환되는 것으로 취급한다
- 이는 Any형의 값에 대해 어떤 연산이나 메서드 호출을 할 수 있고, 그것을 임의의 변수에 대입 할 수 있음을 의미한다
- Any형의 값을 보다 구체적인 형에 대입할 때 형 검사기가 수행되지 않음을 주의해야 한다
- 또한 반환형이나 매개 변수 형이 없는 모든 함수는 묵시적으로 Any기본값을 사용한다 (아래코드)
- 동적으로 형이 지정되는 코드와 정적으로 형이 지정된느 코드를 혼합해야 할 때 Any를 탈출구로 사용할 수 있다

```python
def legacy_parser(text):
    ...
    return data


# 정적 형 검사기는 위의 것이 다음과 같은 서명을 가진 것으로 취급합니다:
def legacy_parser(text: Any) -> Any:
    ...
    return data
```

- Any와 유사하게 모든 형은 object의 서브 형이다. 그러나 Any와는 달리 object는 모든 형의 서브형이 아니다
- 값의 형이 object일 때, 형 검사기가 그것에 대한 거의 모든 연산을 거부하고, 그것을 더 특수한 형의 변수에 대입하는 것이 형 에러임을 의미한다
- `값이 형 안전한 방식으로 모든 형이 될 수 있음을 표시하려면 object를 사용하면 좋다. 값이 동적으로 형지정됨을 표시하려면 Any를 사용하면 좋다`

```python
def hash_a(item: object) -> int:
    # 실패; object에는 'magic' 메서드가 없습니다. 있으면 통과 
    item.magic()
    ...


def hash_b(item: Any) -> int:
    # 형 검사 통과
    item.magic()
    ...


# 형 검사 통과, int와 str이 object의 서브 클래스이기 때문
hash_a(42)
hash_a("foo")

# 형 검사 통과, Any가 모든 형과 호환되기 때문
hash_b(42)
hash_b("foo")
```

### 명목적 대 구조적 서브 타이핑
- 