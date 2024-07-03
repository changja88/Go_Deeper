- 제너레이터는 전통적인 언어와 파이썬을 구분 짓는 또 다른 특징적인ㄴ기능이다
- 이터레이터 패턴을 따르면 왜 언어에서 자동으로 반복을 지원하게 되는지도 알게 된다
    - 이 개념에서 출발하여 제너레이터가 어떻게 코루틴이나 비동기 프로그래밍 같은 기능을 지원하기 위한 기본 기능이 되었는지 알아본다

# 제너레이터 만들기

- 제너레이터는 파이썬에서 고성능이면서도 메모리를 적게 사용하는 반복을 위한 방법으로 PEP-255, 2001년에 소개되었다
- `제너레이터는 한 번에 하나씩 구성요소를 반환하는 이터레이터 객체를 반환하는 함수이다`
    - 제너레이터를 사용하는 주된 목적은 메모리를 절약하는 것이다
    - 거대한 요소를 한꺼번에 메모리에 저장하는 대신 특정 요소를 어떻게 만드는지 아는 객체를 만들어서 필요할 때마다 하나씩만 가져오는 것이다
    - 이 기능은 하스켈과 같은 다른 함수형 프로그래밍 언어가 제공하는 것과 비슷한 방식으로 게이른 연산(lazy computation)을 통해 무거운 객체를 사용할 수 있도록 한다
    - 게으른 연산의 특성을 가졌기 떄문에 무한 스퀀스를 사용할 수도 있다

## 제너레이터 개요

- 두 개의 필드만 있는 CSV 파일이 있다고 가정해보자
    - <purchate_date>, <price>
    - 모든 구매 정보를 받아 필요한 지표를 구해주는 객체를 만들어 보자
    - 최솟값이나, 최댓값 같은 지표는 min(), max()같은 내장 함수를 사용하여 쉽게 구할 수 있다
    - 그러나 어떤 지표는 단번에 구할 수 없고 모든 구매 이력을 반복해야만 한다

```python
class PurchaseStats:
    def __init__(self, purchases):
        self.purchases = iter(purchases)
        self.min_price: float = None
        self.max_price: float = None
        self._total_purchases_price: float = 0.0
        self._total_purchases = 0
        self._initialize()

    def _initialize(self):
        try:
            first_value = next(self.purchases)
        except StopIteration:
            raise ValueError("더이상 값이 없음")
        self.min_price = self.max_price = first_value
        self._update_avg(first_value)

    def process(self):
        for purchase_value in self.purchases:
            self._update_min(purchase_value)
            self._update_max(purchase_value)
            self._update_avg(purchase_value)
        return self

    def _update_min(self, new_value: float):
        if new_value < self.min_price:
            self.min_price = new_value

    def _update_max(self, new_value: float):
        if new_value > self.max_price:
            self.max_price = new_value

    @property
    def avg_price(self):
        return self._total_purchases_price / self._total_purchases

    def _update_avg(self, new_value: float):
        self._total_purchases_price += new_value
        self._total_purchases += 1

    def __str__(self):
        return (
            f"{self.__class__.__name__}({self.min_price}, "
            f"{self.max_price}, {self.avg_price})"
        )
```

- 지표를 구하는 코드 자체는 간단한다. for 루프의 각 단계에서 각 지표를 업데이트 하기면 하면 된다
    - 이 객체는 모든 구매 정보(purchases)를 받아서 필요한 계산을 한다
    - 이제 이 모든 정보를 코드에서 어딘가에 담아서 반환해주는 함수를 만들면 된다

```python
def _load_purchases(filename):
    purchases = []
    with open(filename) as f:
        for line in f:
            _, price_raw = line.partition(";")
            purchases.append(float(price_raw))
    return purchases
```

- 위 코드는 정상적인 결과를 반환한다
    - 파일에서 모든 정보를 읽어서 리스트에 저장한다
    - 그러나 성능에 문제가 있다. 파일에 상당히 많은 데이터가 있다면 로드하는데 시간이 오래 걸리고 메인 메모리에 담지 못할 만큼 큰 데이터일 수도 있다

```python
def load_purchases(filename):
    with open(filename) as f:
        for line in f:
            _, price_raw = line.partition(";")
            yield float(price_raw)
```

- 해결책은 제너레이터를 만드는 것이다
    - 파일의 전체 내용을 리스트에 보관하는 대신에 필요한 값만 그때그때 가져오는 것이다
    - 결과를 담을 리스트가 필요 없어졌으며 return 문 또한 사라졌다
    - 이 런 함수를 제너레이터 함수 또는 단순히 제너레이터라고 부른다
    - 즉, 파이썬에서 어떤 함수라도 yield키워드를 사용하면 제너레이터 함수가 된다
- 이터러블을 사용하여 for 루프와 쉽게 호환이 가능한 강력한 추상화를 이룰 수 있다
    - 이터러블 인터페이스를 따르기만 하면 투명하게 객체의 요소를 반복 가능한 것이다

## 제너레이터 표현식

- 제너레이터는 이터레이터이므로 리스트나 튜플, 세트처럼 많은 메모리를 필요로하는 이터러블이나 컨테이너의 대안이 될 수 있다
- 컴프리헨션(comprehension)에 의해 정의될 수 있는 리스트나 세트, 사전처럼 제너레이터도 제너레이터 표현식으로 정의될 수 있다
    - 물론 제너레이터 표현식을 제너레이터 컴프리헨션으로 불러야 한다는 주장도 있다
    - 대괄호를 괄호로 교체하면 표현식의 결과로부터 제너레이터 생성된다
    - 제너레이터 표현식은 sum()이나 max()와 같은 이터러블 연산이 가능한 함수에서 직접 사용할 수도 있다

```python
[x ** 2 for x in range(10)]
(x ** 2 for x in range(10))  # -> <generator object <genexpr>> at 0x...>
sum(x ** 2 for x in range(10))  # 285
sum([x ** 2 for x in range(10)])  # 이렇게 하지 말자
```

- 위 코드의 권장 사항이 의미하는 바는 제너레이터를 사용할 수 있는 함수에 리스트를 전달하지 말자는 것이다
- 제너레이터 표현식도 컴프리헨션처럼 변수에 할당한 다음에 다르 ㄴ곳에서 사용할 수 있다
    - `차이점은 리스트는 여러 번 재사용할 수 이씨만, 제너레이터는 ㅈ재사용할 수 없다`
    - 따라서 꼭 한 한번만 사용하는지 확인을 해야 한다
- 일반적으로는 새로운 제너레이터 표현식을 만들어서 모두 소비한 다음에 다시 새로운 제너레이터 표현식을 만든다
    - 이렇게 표현식을 연결하면 메모리를 절약하면서 각각의 코드에 다른 표현식을 사용하기 떄문에 보다 명료한 코드가 될 수 있다
    - 예를 들어, 하나의 이터러블에 대해서 여러 필터를 적용하는 경우 여러 제너레이터 표현식을 연결하면 유용하게 사용할 수 있다

# 이상적인 반복

- 파이썬에서 반복을 할 때 유용하게 사용할 수 있는 관용적인 코드를 살펴본다

## 관용적인 반복 코드

```python
list(enumerate('abcdef'))  # [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f')]
```

- enumerate는 이터러블을 입력 받아서 인덱스 번호와 원본의 원소를 튜플 형태로 변환하여 enumerate 객체르 반환한다

```python
class NumberSequence:
    def __init__(self, start=0):
        self.current = start

    def next(self):
        current = self.current
        self.current += 1
        return current


seq = NumberSequence()
seq.next()  # 0
seq.next()  # 1

seq2 = NumberSequence(10)
seq2.next()  # 10
seq2.next()  # 11

list(zip(NumberSequence(), "abcdef"))
"""
Traceback (most recent call last):
...
TypeError: zip argument #1 must support iteration
"""
```

- 위 코드는 좀 더 저수준에서 위 코드를 만든 것이다
    - 이 객체는 단순히 시작 값을 입력하면 무한 시퀀스를 만든다
    - 하지만 이 코드로 enumerate() 함수를 사용하도록 재작성할 수는 없다
    - 왜냐하면 일반 파이썬의 for 루프를 사용하기 위한 인터페이스를 지원하지 않기 떄문이다
    - 문제는 NumberSequence가 반복을 지원하지 않는다는 것이다
        - 이 문제를 해결하려면 __iter__매직 메서드를 구현하여 객체가 반복 가능하게 만들어야 한다

```python
class SequenceOfNumbers:
    def __init__(self, start=0):
        self.current = start

    def __next__(self):
        current = self.current
        self.current += 1
        return current

    def __iter__(self):
        return self


list(zip(SequenceOfNumbers(), "abcdef"))  # [(0, 'a'), (1, 'b'), (2, 'c'), (3, 'd'), (4, 'e'), (5, 'f')]
seq = SequenceOfNumbers(100)
next(seq)  # 100
next(seq)  # 101

word = iter("hello")
next(word)  # 'h'
next(word)  # 'e'
```

- 위 코드처럼 작성하면 요소를 반복할 수 있을 뿐 아니라 .next() 메서드를 호출할 필요도 없다
- 이터레이터 프로토콜은 __iter__와 __next__메서드에 의존한다
- 파이썬에서 이러한 프로토콜을 사용했을 때 장점이 있다
    - 파이썬에 익숙한 모든 사람이 이러한 인터페이스를 알고 있을 것이므로, 이러한 프로토콜이 일종의 표준 계와과 같은 형태로 동작한다는 점이다
    - `이러한 프로토콜이 일종의 표준 계약과 같은 형태로 동작한다`

### next()함수

- next()내장 함수는 이터레이터를 다음 요소로 이동시키고 기존의 값을 반환한다. 더 이상의 값을 가지고 있지 않다면 StopIteration 예외가 발생한다
    - 이 문제를 해결하려면 예외 처리를 하거나 next()함수의 두 번째 파라미터에 기본값을 제공할 수도 있다
    - 여러 제너레이터 표현식을 조합하면 이터러블에서 어떤 조건을 만족하는 첫 번째 요소를 찾을 때 next()함수가 매우 유용한 수단일 수 있다

### 제너레이터 사용하기

```python
def sequence(start=0):
    while True:
        yield start
        start += 1
```

- 앞의 코드는 제너레이터를 사용하여 후러씬 간단하게 작성할 수 있다. 제너레이터를 사용하면 클래스를 만드는 대신 yield하는 함수를 만들면 된다
- 제너레이터 함수가 호출되면 yield문장을 만나기 전까지 실행된다. 그리고 값을 생성하고 그 자리에서 멈춘다

### itertools

- 이터레이터, 제너레이터, itertools와 관련하게 가장 좋은 점은 서로 연결하여 새로운 객체를 만들 수 있다는 것이다

```python
def process(self):
    for purchase in self.purchases:
        if purchase > 1000.0:
            ...
```

- 위 코드는 파이썬스럽지 않을 뿐 아니라 너무 엄격하다

```python
from itertools import islice

purchases = islice(filter(lambda p: p > 1000.0, purchases), 10)
stats = PurchaseStats(purchases).process()
```

- 위 코드처럼 필터링을 해도 메모리의 손해는 없다. 왜냐하면 모든 것이 제너레이터이므로 게이르게 평가된다
    - 즉 마치 전체에서 필터링한 값으로 연산을 한 것처럼 보이지만, 실제로는 하나씩 가져와서 모든 것을 메모리에 올릴 필요가 없는 것이다
    - `제너레이터를 사용하면 메모리를 덜 사용하지만 CPU자원은 더 많이 사용할 수도 있다`
    - 그러나 유지보수성을 높이면서 메모리에서 많은 객체를 처리해야 하는 상황이라면 대부분 허용되는 수준이다

### 이터레이터를 사용한 코드 간소화

#### 여러 번 반복하기

```python
def process_purchases(purchases):
    min_, max_, avg = itertools.tee(purchases, 3)
    return min(min_), max(max_), median(avg)
```

- itertools.tee 는 원래의 이터러블을 세 개의 새로운 이터레이터로 분할한다
    - 다만 가장 앞서 나가는 for 문을 기준으로 위치가 이동하는 셈이다
    - 따라서 for 문이 2개 있다고 해서 전체 데이터가 갑자기 2배로 복사되는 것은 아니지만, 적어도 어느 인덱스에서의 요소에 대해서는 2배의 메모를 사용하게 된다
    - 즉, tee 함수가 제너레이터를 활용했따고 해서 성능차이가 전혀 없는 것은 아니다
    - 개별 요소의 크기가 작다면 상관이 없게씾만 개별 요소가 크고 이터러블을 여러 개 복사 해야 한다면 유의해야 한다

#### 중첩 루프

- 경웨 따라서 1차원 이상을 반복해서 값을 찾아야 할 수 있다
    - 가장 쉬운 방법은 중첩루프가 있다. 값을 찾으면 순환을 멈추고 break를 호출해야 하는데 이런 경우 한 단계가 아니라 두 단계 이상 벗어나야 하므로 정상적으로 동작하지 않는다
    - 이런경우 가장 좋은 방법은 가능하면 중첩을 풀어서 1차원 루프로 만드는 것이다

```python
def search_nested_bad(array, desired_value):
    coords = None
    for i, row in enumerate(array):
        for j, cell in enumerate(row):
            if cell == desired_value:
                coords = (i, j)
                break
        if coords is not None:
            break
    if coords is None:
        raise ValueError(f"{desired_value} 값을 찾을 수 없음")
    logger.info("[%i, %i]에서 값 %r 발견", *coords, desired_value)
    return coords
```

- 위와 같은 코드는 피해야 한다

```python
def _iterate_array2d(array2d):
    for i, row in enumerate(array2d):
        for j, cell in enumerate(row):
            yield (i, j), cell


def search_nested(array, desired_value):
    try:
        coord = next(
            (coord for coord, cell in _iterate_array2d(array)
             if cell == desired_value)
        )
    except StopIteration:
        raise ValueError(f"{desired_value} 값을 찾을 수 없음")
    logger.info("[%i, %i]에서 값 %r 발견", *coord, desired_value)
    return coord
```

- 위 코드는 종료 플래그를 사용하지 않은 보다 간단하고 컴팩트한 형태의 예이다
- 제너레이터가 단순히 메모리를 절약하기 위한 수단이 아니라 그 이상의 용도로 활용될 수 있다는 점을 알아야 한다
    - 즉, 반복을 추상화의 수단으로 활용할 수 있다
    - 클래스나 함수를 사용하지 않더라도 파이썬 구문을 사용하여 추상화를 할 수도 있다
    - 이터레이터를 사용해 같은 for문 뒤로 로직을 숨길 수 있다

### 파이썬의 이터레이터 패턴

- 제너레이터는 이터러블 객체의 특별한 경우이지만 파이썬의 반복은 제너레이터 이상의 것으로 훌륭한 이터러블 객체를 만들게 되면 보다 효율적이고 컴팩트하고 가독성이 높은 코드를 작성할 수 있다

#### 이터레이션 인터페이스

- 이터러블은 반복을 지원하는 객체로 크게 보면 아무 문제 없은 for ... in .. 루프를 실행할 수 있다는 것을 뜻한다
    - 그러나 이터러블과 이터레이터는 다르다
    - `일반적으로 이터러블은 단지 반복할 수 있는 어떤 것을 말하고, 실제 반복 작업은 이터레이터에 의해서 이뤄진다`
- 이터레이터는 내장 next()함수 호출시 일련의 값에 대해 한 번에 하나씩만 어떻게 생성하는지 알고 있는 객체이다
    - 이터레이터를 호출하지 않은 상태에서 다음 값을 요청 받기 전까지 그저 얼어 있는 상태일 뿐이다
    - 이러한 의미에서 모든 제너레이터는 이터레이터이다

| 파이썬개념 | 매직메서드    | 비고                                                                                                            |
  |-------|----------|---------------------------------------------------------------------------------------------------------------|
| 이터러블  | __iter__ | 이터레이터와 함계 반복 로직을 만든다<br/>이것을 구현한 객체는 for...in..구문에서 사용할 수 있다                                                  
| 이터레이터 | __next__ | 한 번에 하나씩 값을 생산하는 로직을 정의힌다<br/> 더이상 생산할 겂이 없는 경우는 StopIteration예외를 발생시킨다<br/>내장 next()함수를 사용해 하나씩 값을 읽어 올 수 있다 |

```python
class SequenceIterator:
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step

    def __next__(self):
        value = self.current
        self.current += self.step
        return value


si = SequenceIterator(1, 2)
next(si)  # 1
next(si)  # 3
next(si)  # 5

for _ in SequenceIterator(): pass
"""
...
Traceback (most recent call last):
    ...
TypeError: 'SequenceIterator' object is not iterable
"""
```

- 위 코드는 이터러블하지 않은 이터레이터 객체의 예이다
    - 시퀀스에서 하나씩 값을 가져올 수 있지만 반복할 수는 없다

#### 이터러블이 가능한 시퀀스 객체

```python
class MappedRange:
    """특정 숫자 범위에 대해 맵으로 변환"""

    def __init__(self, transformation, start, end):
        self._transformation = transformation
        self._wrapped = range(start, end)

    def __getitem__(self, index):
        value = self._wrapped.__getitem__(index)
        result = self._transformation(value)
        logger.info("Index %d: %s", index, result)
        return result

    def __len__(self):
        return len(self._wrapped)


mr = MappedRange(abs, -10, 5)
```

- 객체가 시퀀스인 경우(__getitem__(), __len__()을 구현한 경우) 반복 가능하다
    - 이 경우 인터프리터는 IndexError예외가 발생할 떄까지 순서대로 값을 제공한다
    - 위 코드는 일반적인 for 루프를 통해서만 반복 가능한 객체를 설명하기 위한 것이다
        - next(mr)의 형태로 접근하면 에러가 발생한다

# 코루틴(coroutine)

- 코루틴의 핵심은 특정 싲머에 실행을 일시 중단했다가 나중에 재시작할 수 있는 함수를 만드는 것이다
    - 이런 기능 덕분에 프로그램은 다른 코드를 디스패치 하기 위해 기존 코드를 중지했다가, 나중에 다시 원래의 위치에서 재시작할 수 있다
- 제너레이터를 코루틴으로 활용할 수도 있다
    - 코루틴을 지원하기 위해 PEP-342에 추가된 기본 메서드는 다음과 같다
        - .close
        - .throw(exZ_type[, ex_value[, ex_traceback]])
        - .send(value)
- 파이썬은 코루틴을 생성하기 위해 제너레이터를 활용한다
    - 제너레이터는 중지 가능한 객체이므로, 자연스럽게 코루틴이 되기 위한 좋은 성질을 가지고 있다
    - 하지만 제너레이터만으로는 코루틴을 만들기에 충분하지 않아서 이러한 메서드가 추가되었다
    - 코드를 일시 중단하는 것만으로는 충분하지 않고 그것과 통신하는 수단이 필요하기 때문이다

## 제너레이터 인터페이스 메서드

### close()

```python
def stream_db_records(db_handler):
    try:
        while True:
            yield db_handler.read_n_records(10)
    except GeneratorExit:
        db_handler.close()


streamer = stream_db_records(DBHandler("testdb"))
next(streamer)  # [(0, 'row 0'), (1, 'row 1'), (2, 'row 2'), (3, 'row 3'), (4, 'row 4'), ...]
next(streamer)  # [(0, 'row 0'), (1, 'row 1'), (2, 'row 2'), (3, 'row 3'), (4, 'row 4'), ...]
streamer.close()  # INFO:...:'testdb' 데이터베이스 연결 종료
```

- 이 메서드를 호출하면 제너레이터에서 GeneratorExit 예외가 발생한다
    - 이 예외를 따로 처리하지 않으면 제너레이터가 더 이상 값을 생성하지 않으며 반복이 중지된다
    - 이 예외는 종료 상태를 지정하는데 사용될 수 있다
    - 코루틴이 일종의 자우너 관리를 하는 경우 이 예외를 통해서 코루틴이 보유한 모든 자원을 해제할 수 있다
    - 일반적으로 컨텍스트 관리자를 사용하거나 finally 블록에 코드를 배치하는 것과 비슷하지만 이 예외를 사용하면 보다 명확하게 처리할 수 있다
- 제너레이터를 호출할 때마다 데이터베이스 핸드러에서 얻은 10개의 레코드를 반환하고, 명시적으로 반복을 끝내기 위해 close()를 호출하면 데이터베이스 연결도 함께 종료된다
    - 이 메서드는 리소를 정리하기 위해 사용하는 것으로, 컨텍스트 관리자를 사용하지 않았거나 하여 자동으로 정리가 어려운 경우에 수동으로 리소스를 해제하기 위해 호출한다

## thow(ex_type[, ex_value[, ex_traceback]])

```python
class CustomException(Exception):
    """처리하려는 에러 유형"""


def stream_data(db_handler):
    while True:
        try:
            yield db_handler.read_n_records(10)
        except CustomException as e:
            logger.warning("%r 에러 발생 후 계속 진행", e)
        except Exception as e:
            logger.error("%r 에러 발생 후 중단", e)
            db_handler.close()
            break


streamer = stream_data(DBHandler("testdb"))
next(streamer)  # [(0, 'row 0'), (1, 'row 1'), (2, 'row 2'), (3, 'row 3'), (4, 'row 4'), ...]
next(streamer)  # [(0, 'row 0'), (1, 'row 1'), (2, 'row 2'), (3, 'row 3'), (4, 'row 4'), ...]
streamer.throw(CustomException)
"""
WARNING:CustomException 에러 발생 후 계속 진행
[(0, 'row 0'), (1, 'row 1'), (2, 'row 2'), (3, 'row 3'), (4, 'row 4'), ...]
"""
streamer.throw(RuntimeError)
"""
ERROR:RuntimeError() 발생 후 중단
INFO:'testdb' 데이터베이스 연결 종료
Traceback (most recent call last):
...
StopIteration
"""

```

- 이 메서드는 제너레이터가 중단된 현재 위치에서 예외를 던진다
    - 제너레이터가 예외를 처리했으면 해당 except 절에 있는 코드가 호출되고, 예외를 처리하지 않았으면 에외가 호출자에게 전파된다
    - 도메인에서 처리하고 있는 CustomException 예외를 받은 경우 제너레이터는 계속 진행된다. 그러나 나머지 예외는 Exception으로 넘어가서 데이터베이스 연결을 종료하고 반복도 종료하게 된다

## send(value)

```python
def stream_db_records(db_handler):
    retrieved_data = None
    previous_page_size = 10
    try:
        while True:
            page_size = yield retrieved_data
            if page_size is None:
                page_size = previous_page_size
            previous_page_size = page_size
            retrieved_data = db_handler.read_n_records(page_size)
    except GeneratorExit:
        db_handler.close()
```

- 위 코드는 이제 읽어올 개수를 파라미터로 받도록 수정했다
    - 안타깝게도 next()함수는 이러한 옵션을 제공하지 않는다
    - 이럴때 이제 send()메서드를 통해 인자 값을 전달 할 수 있다
    - `이 메서드는 사실 제너레이터와 코루틴을 구분하는 기준이 된다`
    - send()메서드를 사용했다는 것은 yield 키워드가 할당 구문의 오른쪽에 나오게 되고 인자 값을 받아서 다른 곳에 할당할 수 있음을 뜻한다
    - 코루틴에서는 일반적으로 receive = yield produced 와 같은 형태로 yield 키워드를 사용한다
- receive = yield produced
    - 이 경우 yield 키워드는 두 가지 일을 한다
    - 하나는 produced 값을 호출자에게 보내고 그곳에 멈추는 것이다. 호출자는 next()메서드를 호출하여 다음 라운드가 되었을 떄 값을 가져올 수 있다
    - 다르 하나는 거꾸로 호출자로부터 send()메서드를 통해 전달된 produced값을 받는 것이다. 이렇게 입력된 값은 receive 변수에 할당된다
- 코루틴에 값을 전송하는 것은 yield 구문이 멈춘 상태에서만 가능하다
    - 그렇게 되려면 일단 코루틴을 해당 상태까지 이동시켜야 한다
    - 코루틴이 해당 상태로 이동하는 유일한 방법은 next()를 호출하는 것이다
    - 즉, 코루틴에게 무엇인가를 보내기 전에 next()메서드를 적어도 한번은 호출해야 한다는 것을 의미하며, 그렇지 않은 경우 아래와 같은 에러가 발생한다

```python
def coro():
    y = yield


c = coro()
c.send(1)
"""
Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
TypeError: can't send non-None value to a just-started generator
"""
```

```python
def stream_db_records(db_handler):
    retrieved_data = None
    page_size = 10
    try:
        while True:
            page_size = (yield retrieved_data) or page_size
            retrieved_data = db_handler.read_n_records(page_size)
    except GeneratorExit:
        db_handler.close()
```

- 위 코드는 보다 간결하고 이해하기 쉽다
    - yield 주변의 관호는 해당 문장이 함수를 호출하는 것처럼 사용되고 page_size와 비교할 것이라는 점을 명확히한다
    - next()를 반드시 호출해야 한다는 것을 기억할 필요 없이 코루틴을 생성하자마자 바로 사용할 수 있다면 훨씬 편할 것이다

```python
@prepare_coroutine
def auto_stream_db_records(db_handler):
    retrieved_data = None
    page_size = 10
    try:
        while True:
            page_size = (yield retrieved_data) or page_size
            retrieved_data = db_handler.read_n_records(page_size)
    except GeneratorExit:
        db_handler.close()


streamer = auto_stream_db_records(DBHandler("testdb"))
len(streamer.send(5))  # 5
```

- PYCOOK의 저자는 이를 해결해줄 데코레이터를 고안했다
    - 이 데코레이터의 목적은 코루틴을 좀 더 편리하게 하는 것으로 위와 같이 자동으로 초기화를 해준다
- 하지만 최신 파이썬을 사용한다면 직접 코루틴을 작성할 일은 많지 않을 것이다. 새로운 구문이 생겼기 때문이다

## 코루틴 고급 주제

- 코루틴은 사실 진보된 제너레이터라고 할 수 있다. 코루틴을 동시에 실행한다거나 하는 등의 추가 기능이 필요하다
- 애플리케이션의 로직이 복잡해지면 예외 처리는 물론이고 서브 코루틴의 값을 어디에서든 사용하도록 해야 하고 여러 코루틴을 스케쥴링해야한다
    - 이러한 일을 더 간편하게 하기 위해 제너레이터를 더 확장해야 한다
    - PEP-380에서 이러한 문제를 해결하기 위해 yield from 구문을 도입하고 값을 반환하도록 하였다

### 코루틴에서 값 반환하기

- 앞서 본것처럼 반복이란 StopIteration 예외가 발생할 때까지 next() 메서드를 계속해서 호출하는 메커니즘을 말한다
- 코루틴은 기술적으로는 제너레이터이지만 반복을 염두해 두고 만든 것이 아니라 나중에 코드가 실행될 때까지 코드의 실행을 멈추는 것을 목표로한다
    - 즉, 일반적으로 반복보다는 상태를 중단하는데 초점을 맞추고 있다
    - 코루틴이 정보를 처리하고 실행을 일시 중단한다는 점에서 코루틴을 경량 스레드 또는 그린 스레드라고 생각할 수 있다
    - 그러나 제너레이터가 일반함수는 아니므로 단지 value = generator() 형태로 호출하는 것은 제너리이터를 만들었을 뿐 아무것도 하지 않은 상태라는 것에 주의해야 한다
- 제러레이터가 값을 반환하게 하려면 어떻게 해야할까?
    - 분명 반복을 중단한 뒤에 값을 가져올 수 있을 것이다
    - 제너레이터에서 값을 반환(return)하면 반복이 즉시 중단된다. 문법의 통일성을 위해 StopItertation예외는 계속 발생한다
    - 그리고 반환하려는 값은 exception 객체에 저장된다 . 이제 해당 값을 처리하는 책임은 호출자에게 있다

```python
def generator():
    yield 1
    yield 2
    return 3


value = generator()
next(value)  # 1
next(value)  # 2
try:
    next(value)  # 3
except StopIteration as e:
    print(f'최종 반환값 : {e.value}')
```

- 위 메커니즘은 코루틴이 값을 반환하도록 하는 데 사용된다
    - PEP-380 이전에는 이렇게 하는 것이 아무 의미가 없었고, 제너레이터 앞에서 return 문을 사용하려고 하면 문법 오류가 발생했었다
    - 그러나 이제 반복이 끈날 때 최종 값을 반환할 수 있고, 그 값은 반복이 끝날 때 발생하는 StopIteration 예외에 저장된다
    - 이렇게 하는 것은 깔끔한 방법은 아니지만 완벽하게 하위 호환이 되기 때문에 제너레이터의 인터페이스를 바꾸지 않아도 되는 장점이 있다

### 작은 코루틴에 위임하기 - yield from 구문

- 값을 반환하는 기능 자체는 언어에서 지우너해주지 않으면 조금 귀찮은 부분이 있다
    - 이 부분을 개선해주기 위한 구문이 바로 yield from 이다
    - value = genertor() 구문은 동작하지않지만 value = yield from generator()는 동작한다

#### 가장 간단한 yield from 사용 예

```python
def chain(*iterables):
    for it in iterables:
        for value in it:
            yield value
```

- 위 코드는 여러 이터러블을 받아서 모두 이동한다

```python
def chain(*iterables):
    for it in iterables:
        yield from it
```

- 위 코드 처럼 yield from 구문을 사용하면 서브 제너레이터에서 직접 값을 생산할 수 있으므로 중첩 루프를 피할 수 있다
    - yield from 구문은 어떤 이터러블에 대해서도 동작하며 이것을 사용하면 마치 최상위 제너레이터가 직접 값을 yield 한 것과 같은 효과를 나타낸다

```python
def all_powers(n, pow):
    yield from (n ** i for i in range(pow + 1))
```

- 이렇게 하면 기존의 서브 제너레이터에서 for문을 사용해 값을 생산하는 대신 한 줄로 직접 값을 생산할 수 있으므로 편리하다

#### 서브 제너레이터에서 반환된 값 구하기

- yield from 의 진짜 존재 이유다

```python
def sequence(name, start, end):
    logger.info("%s generator started at %d", name, start)
    yield from range(start, end)
    logger.info("%s generator finished at %d", name, end)
    return end


def main():
    step1 = yield from sequence("first", 0, 5)
    step2 = yield from sequence("second", step1, 10)
    return step1 + step2


g = main()
next(g)
"""
INFO:generators_yieldfrom_2:first generator started at 0
0
"""
next(g)  # 1
next(g)  # 2
next(g)  # 3
next(g)  # 4
next(g)
"""
INFO:generators_yieldfrom_2:first generator finished at 5
INFO:generators_yieldfrom_2:second generator started at 5
5
"""
next(g)  # 6
next(g)  # 7
next(g)  # 8
next(g)  # 9
next(g)
"""
INFO:generators_yieldfrom_2:second generator finished at 10
Traceback (most recent call las):
    File "<stdin>", line 1, in <module>
StopIteration:15
"""
```

- main 제너레이터의 첫 번째 행은 내부 제너레이터로 위임하여 생산된 값을 가져온다
- yield from 구문은 제너레이터를 순환하고 StopIteration예외를 받으면 당시의 종료 값을 반환한다
    - StopIteration의 값은 yield from 문장의 결과 값이 된다
    - 이것은 다음 섹션의 주제와 관련하여 코루틴이 스레드와 유사한 형태를 취할 수 있음을 의미하기 떄문에 강력한 기능이 될 수 있다

#### 서브 제너레이터와 데이터 송수신하기

- 제너레이터는 코루틴처럼 동작할 수 있다. 값을 전송하고 예외를 던지면 코루틴 역할을 하는 해당 제너레이터는 값을 받아서 처리하거나 반드시 예외를 처리해야 한다
- 앞의 예제처럼 서브 제너레이터에 위임한 코루틴에 대해서도 마찬가지다
    - 그런데 수동으로 이런 것들을 처리하려면 매우 복잡할 것이다
    - yield from 에서 자동으로 처리하지 않을 경우의 직접 처리하는 코드는 PEP-380에서 확인할 수 있따

```python
def sequence(name, start, end):
    value = start
    logger.info("%s generator started at %d", name, value)
    while value < end:
        try:
            received = yield value
            logger.info("%s received value %r", name, received)
            value += 1
        except CustomException as e:
            logger.info("%s received exception %s", name, e)
            received = yield "OK"
    return end


g = main()
next(g)  # INFO: first generator started at 0
next(g)  # INFO: first generator received value None 1
g.send("input for first generator")  # INFO: first generator received value 'input for first generator' 2
g.throw(CustomException("custom exception"))  # INFO: first generator received exception 'custom exception''OK'
next(g)  # 2
next(g)  # INFO: first generator received value None 3
next(g)  # INFO: first generator received value None 4
next(g)  # INFO: second generator started at 5
```

- 위 코드는 이상적인 코드는 아니고 동작 메커니즘을 설명하기 위한 용도의 코드이다
    - 이제 main 코루틴을 반복하는 것 뿐 아니라 내부 sequence 제너레이터에서 어ㄸ허게 처리하는지 확인할 수 있다
- 주목해야할 점
    - sequence 서브 제너레이터에 값을 보내지 않고 오직 main 제너레이터에 값을 보냈다는 것
    - 실제 값으 ㄹ받는 것은 내부 제너레이터 이다
    - 명시적으로 sequence에 데이터를 보낸 적은 없지만 yield from 을 통해 sequence 에 데이터를 전달한 셈이다
- 이러한 메서드는 yield from 구문과 함께 많은 새로운 기능(스레드에 하는 것과 유사한)을 제공한다
    - 이러한 기능은 다음에 살펴볼 비동기 프로그래밍을 가능하게 한다

# 비동기 프로그램이

- 여러 코루틴이 특정 순서로 동작하도록 스케줄링 할 수 있으며, 일시 정지된 yield from 코루틴과 통신할 수 있다
    - 가장 큰 장점은 논블로킹 방식으로 병렬 I/O작업을 할 수 있다는 것이다
- 코루틴과 제너레이터가 기술적으로는 동일하다는 점이 혼란스럽지만 의미적으로 다르다
    - 효율적인 반복을 원할 때는 제너레이터를 사용하고 논블로킹I/O 작업을 원할 때는 코루틴을 사용한다
- 파이썬 3.5 이전에 코루틴은 @coroutine 데코레이터가 적용된 제너레이터일 뿐이었으며 yield from 구문을 사용해 호출해었다
    - 그러나 이제 코루틴이라는 새로운 타입이 추가되었다
    - 새로운 구문으로 await 와 async def 또한 추가되었다
    - await는 yield from을 대신 하기 위한 용도로 사용되고, 오직 awaitable 객체에 대해서만 동작한다
    - 코루틴 또한 awaitable 객체이다
    - async def는 앞서 소개한 데코레이터를 대신하여 코루틴을 정의하는 새로운 방법이다
        - 이것을 호출하면 코루틴 인스턴스를 반환하는 객체를 만든다
        - async def로 정의된 객체를 호출하면 __await__메서드를 가진 코루틴 객체를 반환한다
- 파이썬에서 비동기 프로그래밍을 한다는 것은 일련의 코루틴을 관리하는 이벤트 루프가 있다는 뜻이다 (asyncio)
- 나머지는 생략
## 비동기 매직 메서드
### 비동기 컨텍스트 관리자
### 다른 매직 메서드
#### 비동기 반복
### 비동기 제너레이터

