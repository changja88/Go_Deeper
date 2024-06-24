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