# 파이썬스러운 코드

- 관용구와 디자인 패턴은 다르다
    - 디자인 패턴은 언어와 무관한 고차원의 개념으로 코드로 즉시 변환되지 않는다
    - 반면에 관용구는 실제 코딩으로 변환된다
- 관용구는 코드이므로 언어에 따라 다르다
    - `파이썬 관용구를 따른 코드를 관용적이라 부르고 파이썬에서는 파이썬스럽다라고 한다`
- 관용적으로 작성하는 이유
    - 관용적인 방식으로 코드를 작성했을 때 일반적으로 더 나은 성능을 낸다
    - 코드도 더 작고 이해하기도 쉽다
    - 개발팀이 동일한 패턴과 구조에 익숙해지면 실수를 줄이고 문제의 본질에 보다 집중할 수 있다

## 인덱스와 슬라이스

- 음수로 뒤에 부터 접근 가능
- ::로 복사 가능
- 특정 구간만 접근 가능
- 스탭으로 접근 가능

### 자체 시퀀스 생성

- 인덱스와 슬라이스는 __getitem__이라는 매직 메서드를 통해서 동작한다
- 시퀀스는 __getitem__과 __len__을 모두 구현한 객체이므로 반복이 가능하다 -> 리스트, 튜플, 문자열 등등

```python
class Items:
    def __init__(self, *values):
        self._values = list(values)

    def __len__(self):
        return len(self._values)

    def __getitem__(self, item):
        return self._values.__getitem__(item)
```

- 위 코드 처럼 클래스가 표준 라이브러리 객체를 감싸는 래퍼인 경우 기본 객체에 가능한 많은 동작을 위임할 수 있다
    - 즉, 클래스가 리스트의 래퍼인 경우 리스트의 동일한 메서드를 호출하여 호환성을 유지할 수 있다
- 클래스가 시퀀스임을 선언하기 위해 collections.abc 모듈의 Sequence 인터페이스를 구현해야 한다
    - 표준 데이터 타입처럼 동작하게 하려면 이 모듈을 구현하는 것이 좋다
    - 이러한 인터페이스를 상속받으면 해당 클래스가 어떤 클래스인지 바로 알 수 있으며, 필요한 요건들을 강제로 구현하게 되기 때문이다
- 다른 방법으로는 상속을 사용할 수도 있다
    - 이 경우는 collections.UserList 부모 클래스를 상속해야 한다
- 래퍼도 아니고 내장 객체를 사용하지도 않는 사용자 정의 클래스에 __getitem__을 구현하려는 경우 파이썬스러운 접근 방식을 따르게 위해 몇 가지를 고려해야 한다
    - 범위로 인덱싱하는 결과는 해당 클래스와 같은 타입의 인스턴스여야 한다 -> ex. 리스트의 일부 역시도 리스트이다
    - slice에 의해 제공된 범위는 파이썬이 하는 것처럼 마지막 요소는 제외해야 한다
    - 즉 위 두사항을 지켜서 일관성을 유지해야 한다

## 컨텍스트 관리자(context manager)

- 켄텍스 관리자는 패턴에 잘 대응되기 때문에 매우 유용하다
    - 사전 조건과 사후 조건이 있는 일부 코드를 실행해야 하는 상황에 적합
    - 일반적으로 리소스 관리와 관련하여 컨텍스트 관리자를 자주 볼 수 있다
- 컨텍스트 관리자 구성
    - __enter__, __exit__ 두 개의 매직 메서드로 구성된다
    - with 문은 __enter__ 메서드를 호출하고 이 메서드가 무엇을 반환하든 as 이후에 지정된 변수에 할당된다
    - 사실 __enter__ 메서드가 특정한 값ㅇ르 반환할 필요는 없다. 값을 반환하더라도 필요하지 않으면 변수에 할당하지 않아도 된다
    - 실행 블록의 마지막 문장이 끝나면 컨텍스트가 종료되며 컨텍스트 관리자 객체의 __exit__ 메서드를 호출한다
    - 컨텍스트 관리자 블록 내에 예외 또는 오류가 있어도 __exit__ 메서드는 무조건 호출된다
- 컨텍스트 관리자는 관심사를 분리하고 독립적으로 유지되어야 하는 코드를 분리하는 좋은 방법이다

```python
class DBHandler:
    def __enter__(self):
        stop_database()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        start_database()


with DBHandler():
    db_backup()
```

- 위 예제에서는 DBHandler를 사용한 블록에서 내부 컨텍스트 관리자의 결과를 사용하지 않았다 &rarr; 이 경우에는 __enter__의 반환값이 필요 없다
- __exit__ 메서드의 서명을 봐야 한다
    - 블록에서 발생한 예외를 파라미터로 받는다
    - 블록에 예외가 없으면 모두 None이다
    - 반환 값도 잘 생각해야 한다. 특별한 작업을 할 필요가 없다면 아무것도 반환하지 않아도 된다
        - True를 반환하면 잠재적으로 발생한 예외를 호출자에게 전파하지 않고 멈춘다는 것을 뜻한다 &rarr; 예외를 씹는 거기 때문에 일반적으로 좋지않다

### 컨텍스트 관리자 구현

- __enter__, __exit__ 매직 메서드만 구현하면 해당 객체는 컨텍스트 관리자 프로토콜을 지원할 수 있다
    - 이렇게도 구현할 수 있지만 유일한 방법은 아니다
    - contextlib 모듈을 사용하면 보다 쉽게 구현할 수 있다

```python
import contextlib


@contextlib.contextmanager
def db_handeler():
    try:
        stop_database()
        yield
    finally:
        stop_database()


with db_handeler():
    db_backup()
```

- 위 함수는 yield 문을 사용했으므로 제너레이터 함수가 된다
- 중요한 것은 yield 문의 앞의 모든 것은 __enter__ 메서드의 일부처럼 취급 된다
    - 위 코드에서는 아무 것도 반환 하지 않았다 -> 암묵적으로 None을 반환하는 것과 같다
    - yield문 다음에 오는 모든 것들을 __exit__ 로직으로 볼 수 있다
- 컨텍스트 매니저를 작성하면 기존 함수를 리팩토링하기 쉬운 장점이 있따
    - 일반적으로 어느 특정 객체에도 속하지 않은 컨텍스트 관리자가 필요한 경우 좋은 방법이다
    - 매직 메서드를 추가하면 업무 도메인이 더 얽히게 되며, 책임이 커지고, 어쩌면 하지 않아도 될 것들을 지원해야만 한다
    - 즉 많은 상태를 관리할 필요가 없고 다른 클래스와 독립되어 있는 경우라면 컨텍스트 관리자를 만든 ㄴ것이 좋은 방법이다
- 컨텍스트 관리자를 구현할 수 있는 더 많은 방법이 있으며, 표준 라이브러리 contextlib 패키지에 있다

```python
import contextlib


class dbhandler_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        stop_databse()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        start_database()


@dbhandler_decorator
def offline_backup():
    ...
```

- 컨텍스트 관리자 안에서 실행될 함수에 데코레이터를 적용하기 위한 로직을 제공하는 믹스인 클래스다
- 반면에 컨텍스트 관리자 자체의 로직은 앞서 언급한 매직 메서들르 구현하여 제공해야 한다
- 특징으로는 with 문이 없다는 것이다
    - 함수를 호출하기만 하면 offline_backup 함수가 컨텍스트 관리자 안에서 자동으로 실행된다
    - 이것이 원본 함수를 래핑하는 데코레이터가 하는 일이다
- 위 접근법의 단점은 완전히 독립적인 것이라는 것이다
    - 사실은 좋은 특성이다
    - 데코레이터는 함수에 대해 아무것도 모르고 그 반대도 마찬가지다
    - 하지만 offline_backup에서 꼭 필요한 경우에도 데코레이터 객체에 직접 접근할 수 없다는 것을 의미한다

```python
import contextlib

with contextlib.suppress(DataConversionException):
    parse_data(input_json_or_dict)
```

- contextlib.supress라는 함수의 기능을 보자
    - 안전하다고 확신하는 경우 해당 예외를 무시하는 기능이다
    - try/except 블록에서 코드를 실행하고 예외를 전달하거나 로그를 남기는 것과 비슷하지만 차이점은 supress 메서드를 호출하면 로직에서 자체적으로 처리하고 예외임을 명시한다는 점이다
- 위 코드에서 DataConversionException은 입력 데이터가 이미 기대한 것과 같은 포맷이어서 변환할 필요가 없으므로 무시해도 안전하다는 것을 뜻한다

## 컴프리헨션(Comprehension)과 할당 표현식

```python
numbers = []

for i in range(10):
    numbers.append(run_calculation(i))

numbers = [run_calculation(i) for i in range(10)]
```

- 컴프리헨션은 일반적으로 가독성이 높아지지만 수집한 데이터에 대해서 어떤 변환을 해야 하는 경우라면 오히려 더 복잡해질 수 있다
    - 이런 경우 for 루프라가 더 나은 선택이 될 수 있다
    - 또는 할당 표현식을 사용할 수도 있다`
- 위 코드에서의 컴프리헨션은 list.append를 반복적으로 호출하는 대신 단일 파이썬 명령어를 호출하므로 일반적으로 더 나은 성능을 보인다`
    - dis.dis(myfunc)로 어셈블리 코드를 확인 할 수 있다
- 더 간결한 코드가 항상 더 나은 코드를 의미하지는 않는다

## 프로퍼티, 속성(Attribute)과 객체 메서드의 다른 타입들

- 파이썬은 private이나 protected접근 제어자를 제공하지 않는다

### 파이썬에서의 밑줄

```python
class Connector:
    def __init__(self, source):
        self.source = source
        self._timeout = 60
```

- 위코드에서 _timeout은 connector 자체에서만 사용되고 호출자는 이 속성에 접근하지 않아야 한다 -> private
- 던더를 접두사로 사용하는 것은 객체의 인터페이스를 명확하게 구분하는 파이썬스러운 방식이다

### 프로퍼티

```python
class Coordinate:
    def __init__(self, lat: float, long: float) -> None:
        self._latitude = self._logitude = None
        self.latitude = lat
        self.longitude = long

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, lat_value: float) -> None:
        if lat_value not in range(-90, 90 + 1):
            raise ValueError
        self._latitude = lat_value
```

- 일부 엔티티는 데이터가 특정 값을 가질 경우에만 존재할 수 있고, 잘못된 값을 가진 경우에는 존재할 수 없다
    - 이것이 일반적으로 유효성 검사 메서드를 만드는 이유이다
    - 파이썬은 setter, getter를 사용하면 이를 더 간결하게 캡슐화할 수 있다
- 프로퍼티는 명령-쿼리 분리 원칙(Command and Query Seperation)을 따르기 위한 좋은 방법이다

### 보다 간결한 구문으로 클래스 만들기

```python
R = 26


@dataclass
class RTrieNode:
    size = R
    value: int
    next_: List["RTrieNode"] = field(default_factory=lambda: [None] * R)

    def __post_init__(self):
        if len(self.next_) != self.size:
            raise ValueError(f'리스트(next_)의 길이가 유효하지 않음')
```

- 파이썬에는 객체의 값을 초기화하는 일반적인 보일러플레이트 코드가 있다 (__init__)
    - dataclasses모듈을 사용하여 단순화할 수 있다
- dataclass모듈
    - 클래스의 모든 속성에 대해서 __init__을 작성한 효과가 있다
    - field라는 객체를 제공한다
        - field객체는 해당 속성에 특별한 특징이 있음을 표시한다
        - 예를 들어 리스트처럼 변경 가능한 데이터 타입인 경우, __init__에서 비어있는 리스트를 할당할 수 없고 대신에 None으로 초기화한 다음에 인스턴스마다 적절한 값으로 다시 초기화를 해야한다
        - field객체를 사용하면 default_factory 파라미터에 list 객체를 전달하여 초깃값을 지정할 수 있다
    - __init__블럭에서 진행하고 싶었떤 유효성 검사는 __post_init__이라는 매직 메소드를 통해서 진행할 수 있다

### 이터러블 객체

- 엄밀히 말하면 이터러블은 __iter__매직 메서드를 구현객 객체, 이터레이터는 __next__ 매직 메서드를 구현한 객체를 말한다
    - 객체가 __next__ 나 __iter__ 이터레이터 메서드 중 하나를 포함하는지 여부
    - 객체가 시퀀스이고 __len__ 과 __getitem__을 모두 가졌는지 여부
- 시퀀스도 반복을 할 수 있으므로 for 루프에서 반복 가능한 객체를 만드는 방법은 두 가지가 있다

#### 이터러블 객체 만들기

```python
class DateRangeIterable:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration()
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today


for day in DateRangeIterable(date(2022, 1, 1), date(2022, 1, 5)):
    ...
```

- 객체를 반복하려고 하면 파이썬은 해당 객체의 iter()함수를 호출한다
    - 이 함수는 __iter__메서드가 있는지를 확인하고 있으면 실행한다
- for 루프는 앞서 만든 객체를 사용해 반복을 시작한다
    - 이제 next()함수를 호출하고 next()는 __next__를 호출한다
    - 더 이상 순회가 불가능할 경우 StopIteration 예외를 발생시켜야 한다

```python
def __iter__(self):
    current_day = self.start_date
    while current_day < self.end_date:
        yield current_day
        current_day += timedelta(days=1)
```

- 위 코드의 문제점은 한번 순회를 마치고 나면 다시 순회를 할 수 없다
    - 이터러블 프로토콜이 작동하는 방식 때문이다
    - 간단한 해결 방법은 __iter__에서 self가 아니라 DateRangeIterable를 매번 새로 만들어서 반환하는 방법이 있다
    - 더 좋은 방법은 __iter__에서 제너레이터를 사용하는 방법이다
    - 이러한 형태의 객체를 컨테이너 이터러블이라고 한다 