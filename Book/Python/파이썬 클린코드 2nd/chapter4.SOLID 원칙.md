# 단일 책임 원칙

- 단일 책임 원칙(SRP- Single Responsibility Principle)
- 클래스가 유일한 책임이 있다는 것은 하나의 구체적인 일을 담당한다는 것을 의미하며 따라서 변경이 필요한 이유도 단 하나만 있어야 한다
    - 오직 해당 도메인의 문제가 변경되는 경우에만 클래스를 업데이트해야 한다
    - 다른 이유로 클래스를 업데이트해야 한다면, 그것은 아마 추상화가 잘못 되었거나 해당 클랫흐가 너무 많은 책임을 가지고 있기 때문일 것이다
- 다시 말해 클래스는 작을 수록 좋다, 관심사의 분리 원칙에 대해 살펴본 것처럼 SRP는 응집력과 밀접한 관련이 있다
- `만약 객체의 속성이나 메서드의 특성이 다른 클래스에서 발견이되면 이들을 다른 곳으로 옮겨야 한다`
- `하나의 클래스에 있는 메서드들 중에 상호 베타적이며 서로 관련이 없는 것이 있따면, 이들은 서로 다른 책임을 가지고 있으므로 더 작은 클래스로 분리해야 한다`

## 너무 많은 책임을 가진 클래스

```python
class SystemMonitor:
    def load_activity(self):
        ...

    def identify_events(self):
        ...

    def stream_events(self):
        ...
```

- 이 클래스의 무네점은 독립적인 동작을 하는 메서드를 하나의 인터페이스에 정의했다는 것이다
    - 각 메서드는 클래스의 책임을 대표하고 있으며, 각각의 책임미다 수정 사유가 발생한다 -> 메서드 마다 다양한 변경의 필요성이 생긴다

## 책임 분산

<img src = "./img/IMG_0776.jpg" width = "800" height = "400">

- 위 클래스를 각자의 책임을 가진 클래스로 만들고, 이것의 인스턴스들과 교류하는 하나의 객체를 만드는 것이다
- 어떤 컴포넌트가 있는데 너무 많은 기능을 가지고 있다면, 기능이 계속 확장될 것이라고 예상할 수 있다
    - 이런 경우 책임을 분리하는 것이 좋은 출발점이다
    - 문제는 책임을 분리하는 경계선을 어디로 하느냐이다
    - 이런경우 내부 협업이 어떻게 이뤄지고 있는지, 책임은 어떻게 분산되고 있는지 이해하기 위해 단일 모놀리식 클래스를 먼저 만들어 보면서 시작할 수 있다

# 개방/폐쇄 원칙

- 개방/폐쇄 원칙 (OCP - Open/Close Principle)
- 클래스를 디자인할 때는 유지보수가 쉽도록 로직을 캡슐화하여 확장에는 개방되고 수정에는 폐쇄되도록 해야한다
    - `즉, 새로운 문제가 발생할 경우 새로운 것을 추가만 할 뿐 기존 코드는 그대로 유지해야 한다는 뜻이다`
    - 기존 코드를 수정했다면 그것은 기존 로직이 잘못 디자인되었다는 것을 뜻한다

## 개방/폐쇄 원칙을 따르지 않을 경우 유지보수의 어려움

<img src = "./img/IMG_0777.jpg" width = "900" height = "400">

```python
class Event:
    raw_data: dict


class UnknownEvent(Event):
    ...


class LoginEvent(Event):
    ...


class LogoutEvent(Event):
    ...


class SystemMonitor:
    def __init__(self, event_data):
        self.event_data = event_data

        def identity_event(self):
            if (
                    self.event_data['before']['session'] == 0
                    and self.event_data['after']['session'] == 1
            ):
                return LoginEvent(self.event_data)
            elif (
                    self.event_data['before']['session'] == 1
                    and self.event_data['after']['session'] == 2
            ):
                return LogoutEvent(self.event_data)

            return UnknownEvent(self.event_data)
```

- 이제 시스템에서 발생하는 이벤트를 분류하는 기능을 가지고 있다
- 위 이미지를 보면, 확장 가능한 구조로 보인다
    - 새로운 이벤트가 추가되면 Event의 하위 클래스를 추가하고 SystemMonitor는 새로운 유형의 이벤트를 처리할 수 있는 것처럼 보인다
    - 그러나 자세히 살펴보면 새로운 유형을 판단하는 로직은 SystemMonitor의 identity안에서 이뤄지기 때문에 SystemMonitor는 새로운 유형의 이벤트에 완전히 종속되어 있다
- UnknownEvent는 null 객체 패턴이라고 하며 나중에 살펴본다
- 위 코드의 문제점
    - 이벤트 유형을 결정하는 로직이 단일 메서드에 중아 집중화된다는 점이다. 지원하려는 에벤트가 늘어날수록 이벤드도 커질 것이다
    - 한 가지 일만 하는 것도 아니고 한가지일을 제대로 하지도 못한다
    - 새로운 유형의 이벤트를 시스템에 추가할 때마다 메서드를 수정해야한다
- 즉 분류하려는 구체 클래스와 직접 상호 작용하는 것이 문제다

## 확장성을 가진 이벤트 시스템으로 리팩토링

<img src = "./img/IMG_0778.jpg" width = "900" height = "400">
- 개방/폐쇄 원칙을 따르는 디자인을 하려면 추상화를 해야한다
- SystemMonitor가 추상 클래스 Event와 협력하게 하고, 이벤트에 대응하는 개별 로직은 각 이벤트(구체 클래스)에 위임하는 것이다

```python
class Event:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return False


class UnknownEvent(Event):
    ...


class LoginEvent(Event):
    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return (
                event_data['before']['session'] == 0
                and event_data['after']['session'] == 1
        )


class LogoutEvent(Event):
    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return (
                event_data['before']['session'] == 1
                and event_data['after']['session'] == 0
        )


class SystemMonitor:
    def __init__(self, event_data):
        self.event_data = event_data

    def identity_event(self):
        for event_cls in Event.__subclasses__():
            try:
                if event_cls.meets_condition(self.event_data):
                    return event_cls(self.event_data)
            except KeyError:
                continue
        return UnknownEvent(self.event_data)
```

- 중요한 점은 이제 상호 작용이 추상화를 통해 이뤄지고 있다
    - identity_event는 이제 특정 이벤트 타입과 비교하는 것이 아니고, 일반적인 인터페이스를 가진 제네릭 이벤트와 비교한다
- __subclasses__대신 abc 모듈의 register 메서드를 사용하여 클래스를 등록하거나, 자체적으로 클래스 레지스트리 목록을 관리한 뒤에 조회하는 것도 가능하다

## 이벤트 시스템 확장

<img src = "./img/IMG_0779.jpg" width = "1000" height = "400">

- 이제 개방/폐쇄 원칙을 지키면서 이벤트를 확장할 수 있다

## OCP 최종 정리

- `이 원칙은 다형성의 효과적인 사용과 밀접하게 관련되어 있다`
    - 다형성을 따르는 형태의 계약을 만들고 모델을 쉽게 확장할 수 있는 일반적인 구조로 디자인하는 것이다
- 이 원칙은 유지보수성에 대한 문제를 해결한다 (파급효과 방지)
- `코드를 변경하지 않고 기능을 확장하기 위해서는 보호하려는 추상화에 대해서 적절한 ㅖ쇄를 해야 한다는 것이다`

# 리스코프 치환원칙(LSP)

- 리스코프 치환 원칙(LSP - Liskov substitution principle)
- 설계의 안정성을 높이기 위해 객체가 가져야 하는 일련의 특성을 말한다
- LSP의 요지는 클라이언트가 특별한 주의를 기울이지 않고도 부모 클래스를 대신하여 하위 클래스를 그대로 사용할 수 있어야 한다는 것이다
    - 즉, 클라이언트는 부모 타입 대신에 어떠한 하위 타입을 사용해도 정상적으로 동작해야 한다
    - `클라리언트는 사용하는 클래스의 계층 구조가 변경되는 것에 대해 알 수 없으며, 그러한 변경사항에 대해 완전히 독립적이어야 한다`

<img src = "./img/IMG_0780.jpg" width = "600" height = "300">

- 위 이미지에서 ClientClass는 주의를 기울이지 않고도 모든 하위 클래스의 인스턴스로 작업할 수 있어야한다는 것이다

## 도구를 사용해 LSP 문제 검사하기

- mypy, pylint 같은 도구를 사용해 쉽게 검출할 수 있따

### mypy로 잘못된 메서드 서명 검사

```python
class Event:
    def meets_condition(self, event_data: dict) -> bool:
        return False


class LoginEvent(Event):
    def meets_condition(self, event_data: list) -> bool:
        return bool(event_data)
```

- 위 코드는 mypy를 실행하면 "error: Arguments 1 of "meet_contition" incompatible with supertyp "Event"" 에러를 발생한다
- 위 코드는 LSP를 위반 했다
    - 파생 클래스가 부모 클래스에서 정의한 파라미터와 다른 타입을 사용했기 때문이
- LSP 원칙은 객체 지향 설계의 관점에서도 의미가 있다
    - `서브클래싱을 할 때는 구체화를 해야 하지만 각 서브클래스의 기본 틀은 부모 클래스가 선언하는 것이어야 한다`

## 애매한 LSP 위반 사례

- 어떤 경우는 애매해서 자동화된 도구로 검사하기 애매할 수 있다
    - 계약이 수정되는 경우는 특히 자동으로 감지하기가 더 어렵다

```python
```

- 부모 클래스는 클라이언트와의 계약을 정의한다. 하위 클래스는 그러한 계약을 따라야 한다

```python
class Event:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return False

    @staticmethod
    def validate_precondition(event_data: dict):
        """인터페이스 계약의 사전 조건
        event_data 파리미터가 적절한 형태인지 유효성 검사
        """
        if not isinstance(event_data, Mapping):
            return ValueError()
        for moment in ('bofore', 'after'):
            if moment not in event_data:
                return ValueError()
            if not isinstance(event_data[moment], Mapping)
                raise ValueError()


class SystemMonitor:
    def __init__(self, event_data):
        self.event_data = event_data

    def identify_event(self):
        Event.validate_precondition(self.event_data)
        for event_cls in Event.__subclasses__():
            try:
                if event_cls.meets_condition(self.event_data):
                    return event_cls(self.event_data)
            except KeyError:
                continue
        return UnknownEvent(self.event_data)

```

- 계약은 오직 최상위 레벨의 키 'before', 'after'가 필수이고 그 값 또한 사전타입이어야 한다고 명시되어 있다
    - 따라서 하위 클래스에서 보다 제한적인 파라미터를 요구하는 경우 검사에 통과하지 못한다

```python
class TransactionEvent(Event):
    """시스템에서 발생한 트랜잭션 이벤트"""

    @staticmethod
    def meets_condition(event_data: dict) -> bool:
        return event_data['after'].get('transaction') is not None
```

- TransactionEvent는 올바르게 설계되었다
    - 'transaction'이라는 키에 제한을 두지 않고 사용하고 있다. 그 값이 있을 경우에만 사용하고 필수로 필요한 것은 아니다
    - 그러나 이전에 사용하던 LoginEvent와 LogoutEvent 클래스는 before, after의 session이라는 키를 사용하기 때문에 그대로 사용할 수 없다
    - 이렇게 되면 계약이 깨지고 KeyError가 발생하기 때문에 나머지 클래스를 사용하는 것과 같은 방식으로 클래스를 사용할 수 없다
- 이 문제는 TransactionEvent와 마찬가지로 대괄호 대신 .get()메서드를 사용해서 해결할수 있다

## LSP 최종 정리

- LSP는 객체지향 설계의 핵심이 되는 다형성을 갖ㅇ조하기 떄문에 좋은 디자인의 기초가 된다
- 인터페이스의 메서드가 올바른 계층구조를 갖도록 하여 상속된 클래스가 부모 클래스와 다형성을 유지하도록 하는 것이다
- 즉 LSP가 OCP에 기여한다고 말할 수 있다

# 인터페이스 분리 원칙

- 인터페이스 분리 원칙(ISP - Interface Sergregation Principle)
- "작은 인터페이스"에 대한 가이드라인을 제공한다
- 객체 지향적인 용어로 인터페이스는 객체가 노출하는 메서드의 집합이다
    - 즉 객체가 수신하거나 해석할 수 있는 모든 메시지가 인터페이스를 구성하며, 클라이언트는 이것들을 호출할 수 있다
    - `인터페이스는 클래스의 정의와 구현을 분리한다`
- 파이썬에서 인터페이스는 메서드의 형태를 보고 암시적으로 정의된다
    - 파이썬은 덕 타이핑원리를 따르기 떄문
    - 덕 타이핑은 모든 객체가 자신이 가지고 있는 메서드와 자신이 할 수 있는 일에 의해서 표현된다는 점에서 출발한다
    - `즉, 클래스의 타입, 이름, 속성, 인스턴스 속성에 관계 없이 객체의 본질을 정의하는 것은 궁극적으로 메서드의 형태이다`
- PEP-3119에서 추상 기본 클래스 개념을 도입했다 (ABC)
    - 파생 클래스가 바드시 구현해야 하는 것을 명시적으로 가리키기 위한 유용하고 강력한 도구이다
    - abc모듈에는 가상 서브클래스(virtual subsclass)를 계충 구조의 일부로 등록하는 방법도 포함되어 있다
        - ABC의 register() 메서드를 사용하면 기존 기본 클래스에 파생 클래스를 추가할 수 있다 -> virtual subclass
        - 즉, 오리 처럼 같은걸 오리로 등록 가능 하다

## 너무 많은 일을 하는 인터페이스

<img src = "./img/IMG_0781.jpg" width = "400" height = "200">

- 위 이미지를 인터페이스로 만들려면 파이썬에서는 추상 기본 클래스를 만들고 from_xml, from_josn이라는 메서드를 정의한다
    - 하지만 어떤 클래스는 둘 중 하나만 필요할 수도 있다
    - 이것은 결합력을 높이고 유연성을 떨어뜨리며 클라이언트가 필요하지도 않은 메서드를 구현하도록 한다

## 인터페이스는 작을수록 좋다

<img src = "./img/IMG_0782.jpg" width = "600" height = "300">

- 위 디자인을 사용하면 XMLEventParser에서 파생되는 클래스는 from_xml()메서드만 구현하면 된다.
- 무이제 새로운 작은 객체를 사용해 모든 기능을 유연하게 조랍할 수 있게 되었다
- SRP와 유사하지만 주요 차이점은 ISP는 인터페이스에 대해 이야기하고 있따는 점이다
    - 따라서 이것은 행동의 추상화다
    - 인터페이스가 실제로 구현될 떄까지는 아무것도 정해지 것이 없으므로 변경할 이유가 없다
    - 그러나 이 원칙을 준수하지 않으면 별개의 기능이 결합된 인터페이스를 만들게 된다
    - 이렇게 상속된 클래스는 SDRP 또한 준수할 수 없게 된다

## 인터페이스는 얼마나 작아야 할까?

- 응집력의 관점에서 가능한 단 한 가지 일을 수행하는 작은 인터페이스여야 한다
    - 딱 한가지 메서드만 있어야 한다는 뜻은 아니다

# 의존성 역전

- 의존성 역전 원칙(DIP)
- 코드가 깨지거나 손상되는 취약점으로부터 보호해주는 디자인 원칙을 제시하단다
    - `의존성을 역전 시킨다는 것은 코드가 세부 사항이나 구체적인 구현에 적응하도록 하지 않고, 대신 API같은 것에 적응하도록 하는 것이다`
    - 추상화를 통해 세부 사항에 의존하지 않도록 해야 하지만, 반대로 세부 사항은 추상화에 의존해야 한다
- A가 B(외부)를 사용하는 경우
    - B가 변경되면 원래 코드는 쉽게 깨진다
    - 즉 B가 A에 적응하게 만들어야 한다
    - 이렇게 하려면 인터페이스에 의존적이도록 해야 한다
    - 해당 인터페이스를 준수한는 것은 B의 책임이다
- `일반적으로 구체적인 구현이 추상 컴포넌트보다 훨씬 더 자주 바뀔 것이다. 이런 이유로 추상화를 사용한다`

## 강한 의존성을 가진 예

<img src = "./img/IMG_0783.jpg" width = "400" height = "200">

- Syslog로 데이터를 보내는 방식이 변경되면 EventStreamer를 수정해야 한다
- 만약 다른 데이터에 대해서는 전송 목적지를 변경하거나 새로운 데이터를 추가하려면 stream()메서드를 수정해야한다

## 의존성을 거꾸로

<img src = "./img/IMG_0784.jpg" width = "600" height = "300">

- 위 문제를 해결하려면 EventStreamer를 구체 클래스가 아닌 인터페이스와 대화하도록 하는 것이 좋다
    - 이렇게 하면 인터페이스의 구현은 세부 구현사랑을 가진 저수준 클래스가 담당하게 된다
- EentStreamer는 특정 데이터 대상의 구체적인 구현과 관련이 없어졌다
    - 구현 내용이 바뀌어도 수정할 필요가 없다
- 심지어 런타임 중에도 send()메서드를 구현한 객체의 프로퍼티를 수정해도 여전히 잘 동작한다
    - `이를 동적으로 제공한다고 하여 의존성 주입(dependency injection)이라고 한다`
- 물론 파이썬은 인터페이스 없이 send()메서드를 가지고 있는 다른 객체를 사용해도 잘 동작한다
    - 하지만 이는 파이썬이 너무 유연하여 자주 발생하는 실수를 줄이기 위함이며 클린 디자인을 위한 것이다

## 의존성 주입(Dependency Injection)

```python
class EventStreamer:
    def __init__(self):
        self._target = Syslog()

    def stream(self, events: list[Event]) -> None:
        for event in events:
            self._target.send(event.serialize())

```

- 위 코드는 유연한 디자인이라 할 수 없으며, 인터페이스를 활용하지도 않았다
- 이렇게 구현하면 테스트도 어렵다
    - 테스트를 작성하려면 Syslog의 생성 로직을 수정하거나, 생성한 뒤에 정보를 업데이트 해야한다

```python
class EventStreamer:
    def __init__(self, target: DataTargetClient):
        self._target = target

        def stream(self, events: list[Event]) -> None:
            for event in events:
                self._target.send(event.serialize())
```

- 위 처럼 함으로써 인텊페이스를 사용하고 다형성을 지원하게 되었다
- 이제 초기화 시 인터페이스를 구현하는 어떤 객체도 전달할 수 있으며, 이벤트 처리기가 그런 유형을 모두 처리활 수 있다는 것을 명시적으로 표현할 수 있다
- 이제 테스트도 간단하다
    - Syslog를 사용하고 싶지 않으면, 알맞은 테스트 더블(호환되는 아무거나)을 제공하기면 하면 된다
- 이제 글루 코드에서 보일러 플레이트 코드를 제거할 수 있다
- 만약 설정해야 할 의존성이 많고, 객체 간의 관계가 복잡하다면 명시적으로 이들 간의 관계를 선언하고, 도구에서 초기화하는 것이 좋다
    - 즉, 한 곳에서 생성 방법을 관리하고, 도구가 실제 생성을 담당하도록 하는 것이다
    - 팩토리 객체와 유사하다

# 요약

- 소프트웨어가 후에도 융통성 있게 변화에 적응할 수 있는지를 확인할 방법은 없다
    - 따라서 원칙에 충실해야 한다 