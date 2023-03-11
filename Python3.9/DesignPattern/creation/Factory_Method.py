from abc import ABC, abstractmethod

from DesignPattern.trash import *

################################################################
'''
아래 코드는 무엇이 문제 인가?
'''


def order_pizza(type: str) -> Pizza:
    pizza = None
    if type == 'cheese':
        pizza = CheesePizza()
    elif type == 'greek':
        pizza = GreekPizza()
    elif type == 'peperoni':
        pizza = PeperoniPizza()

    pizza.prepare()
    pizza.bake()
    pizza.cut()
    pizza.box()

    return pizza


'''
- 위 상황만으로는 문제가 있다고 보기 어렵다 
    - Pizza를 준비하는 과정이 변경이 많을지 Pizza를 선택하는 종류의 변경이 많을지는 알 수 없기 때문 
    - 일반적으로는 Interface의 변경은 자주 발생하지 않기 때문에(발생하면 안됨) Pizza를 선택하는 종류의 변경이 변화가 많다고 볼 수는 있음
       
- 위 상황에서 가장 문제가 되는 부분은 인스턴스를 만들 구상 클래스를 선택하는 부분이다
    - ClamPizza를 추가 해야한다면? VeggiePizza를 추가 해야한다면?
    - if문을 추가하거나 삭제 해야한다 -> 개방 폐쇄 원칙에 맞지 않는다  
'''
################################################################
################################################################
'''
무엇을 해야 하는가
- 비교적 변경이 덜 발생하는 부분을 비교적 변경이 자주 발생하는 곳으로 부터 떼어 놔야 한다 -> 캡슐화
- 즉, 캡슐화라는 것은 변경이 자주 발생하는 부분을 모아서 변경이 덜 발생하는 부분으로 부터 격리 시키는 것
'''
################################################################
################################################################
'''
어떻게 캡슐화를 할 것인가
- 객체를 생성하는 부분을 factory로 캡슐화한다
'''


class SimplePizzaFactory:
    def createPizza(type: str) -> Pizza:
        pizza = None
        if type == 'cheese':
            pizza = CheesePizza()
        elif type == 'greek':
            pizza = GreekPizza()
        elif type == 'peperoni':
            pizza = PeperoniPizza()
        return pizza


class PizzaStore:
    def __init__(self, factory: SimplePizzaFactory):
        self.factory = factory

    def order_pizza(self, type: str) -> Pizza:
        pizza = self.factory.createPizza(type)
        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()

        return pizza


'''
- 이 부분까지가 간단한 팩토리(Simple Factory)라고 하며 디자인 패턴이라고 할 수는 없고 자주 쓰이는 관용구에 가깝다
- 이렇게 객체를 생성하는 부분만을 다른 곳(factory)로 넘긴 것이 의미가 있는가?
    - SimplePizzaFactory를 사용하는 곳이 많아 진다면 의미가 있다
    - PizzaStore 에서는 더 이상 구상 객체를 만들 필요가 없다
      
TIP
- createPizza 함수만을 밖으로 빼서 사용하는 것을 정적 팩토리(static factory) 패턴이라고 한다 
- 어떤 객체를 생성하는데 객체를 생성하지 않고 할 수 있다는 장점이 있다
    -> SimplePizzaFactory라는 객체를 생성하지 않고  createPizza 함수만 호출해서 객체를 생성한다
    
- 추가적인 요구사항이 없다면 여기까지만 코드를 작성해도 문제가 전혀 없다!!!
    - 변화가 잦은 객체를 생성하는 부분이 '간단한 팩토리'로 캡슐화가 되어 있기 때문
    - (사실은 문제 있음, 뒤에 나옴) 
'''
################################################################
################################################################
'''
- 아래와 같은 추가 요구 사항이 있다면 어떻게 확장할 것인가?
  요구사항
    - PizzaStore가 성공해서 각 지역특색을 살린 프랜차즈를 운영해야 한다 -> 지역별로 다른 피자를 만들어야 한다 
    - 치즈피자 -> 뉴욕스타일 치즈피자, 시카고 스타일 치즈 피자
- 위에서 배웠던 것처럼(간단한 팩토리)를 여러개 만들어서 해결하면 되지 않을까? 
    - NYPizzaFactory, ChicagoPizzaFacotry, CaliforniaPizzaFactory 사용
'''


class NYPizzaFactory(SimplePizzaFactory):
    def createPizza(type: str) -> Pizza:
        pizza = None
        if type == 'cheese':
            pizza = NYCheesePizza()
        elif type == 'greek':
            pizza = NYGreePizza()
        elif type == 'peperoni':
            pizza = NYPeperoniPizza()
        return pizza


class ChicagoPizzaFactory(SimplePizzaFactory):
    def createPizza(type: str) -> Pizza:
        pizza = None
        if type == 'cheese':
            pizza = ChicagoCheesePizza()
        elif type == 'greek':
            pizza = ChicagoGreePizza()
        elif type == 'peperoni':
            pizza = ChicagoPeperoniPizza()
        return pizza


nyFactory = NYPizzaFactory()
nyStore = PizzaStore(nyFactory)
nyStore.order_pizza('peperoni')

chicago_factory = ChicagoPizzaFactory()
chicago_store = PizzaStore(chicago_factory)
chicago_store.order_pizza('peperoni')

'''
- 정말 문제가 없느가?
    - 문제가 있다
    - 지금 까지는 피자의 "생성"에만 포커스를 맞췄지만 최종적인 목표는 order_pizza이다
        - 즉 최종목표는 피자를 "생성"해서 준비하고, 굽고, 자르고, 포장 하는 것까지 이다
    - 최종목표가 그렇다면 어떤 문제가 있을 수 있느가?
        - 땡땡Factory를 이용해서 피자를 만들 수는 있지만 order_pizza를 완료 하기 위한 순서를 보장 할 수 없다
        - 즉, 떙떙factory에서 피자를 만들고 포장,하고 굽고, 자르고 하는 등 순서로 개똥으로 해서 망할 수 있다
        - 결론적으로 order_pizza라는 목표(order_pizza)를 달성하기 위해서는 Factory에서 생성된 피자를 반드시 정해준 순서로 해야한다
          ( prepare -> bake -> cut -> box 순서가 보장 되어야 한다)
'''
################################################################
################################################################
'''
위 문제를 해결하기 위해서는 어떻게 해야 하는가? 
    - 목표 : 객체의 생성은 유연해야 하지만 생성된 객체에 대해서는 일관된 작업이 보장되어야 한다 
'''


class PizzaStore(metaclass=ABC):
    def order_pizza(self, type: str):
        pizza = self.create_pizza(type=type)

        pizza.prepare()
        pizza.bake()
        pizza.cut()
        pizza.box()

        return pizza

    @abstractmethod
    def create_pizza(self, type: str) -> Pizza:
        pass


class NYPizzaStore(PizzaStore):

    def createPizza(type: str) -> Pizza:
        pizza = None
        if type == 'cheese':
            pizza = NYCheesePizza()
        elif type == 'greek':
            pizza = NYGreePizza()
        elif type == 'peperoni':
            pizza = NYPeperoniPizza()
        return pizza


class ChicagoStore(PizzaStore):

    def create_pizza(self, type: str) -> Pizza:
        pizza = None
        if type == 'cheese':
            pizza = ChicagoCheesePizza()
        elif type == 'greek':
            pizza = ChicagoGreePizza()
        elif type == 'peperoni':
            pizza = ChicagoPeperoniPizza()
        return pizza


'''
무엇이 좋아 졌는가
- order_pizza는 더이상 구상 피자 객체에 의존하지 않는다 (Pizza라는 추상 클래스에 의존한다)
    - order_pizza에서 pizza를 생성하기는 하지만 어떤 종류의 피자인지는 order_pizza는 전혀 알지 못한다   
    - 즉, 구상피자와 피자스토어는 완전히 분리 되어 있다 
'''
################################################################

'''
총정리

팩토리 메소드 패턴(Factory Method Pattern)
### 정의 ###
- 팩토리 메소드 패턴에서는 객체를 생성하기 위한 인터페이스를 정의하는데, 어떤 클래스의 인스턴스를 만들지는 서브클래스에서 결정하게 만든다
  팩토리 메소드 패턴을 이용하면 클래스의 인스턴스를 만드는 일을 서브클래스에게 맡기는 것이다
  
### 목적 ###
- 모든 팩토리 패턴의 목적은 객체 생성의 캡슐화!
- 팩토리 메소드 패턴에서는 서브클래스에서 어떤 클래스를 만들지를 결정하게 함으로써 객체 생성을 캡슐화 한다

### 수호 디자인 원칙 ###
- 의존성 역전 원칙 (Dependency Inversion Principle)
    - 추상화된 것에 의존하도록 만들어라. 구상 클래스에 의존하도록 만들지 말아라 
    - PizzaStore가 구체 피자(CheesePizza, PeperoniPizza)에 의존하지 않는다 
    - PizzaStoresms 추상화된 Pizza에 의존한다 -> 추상화 레벨이 맞는다
    - 의존성 역전 
        - PizzaStore -> 구체 피자 (변화가 적은 PizzaStore가 변화가 많은 구체 피자에 의존하고 있음)
        - PizzaStore -> Pizza <- 구체 피자 
        - 왜 역전이라고 하나 
            - Pizza라는 추상화를 통해서 왼쪽에서 오른쪽으로 흐르던 화살표가 오른쪽에서 왼쪽으로 바뀌었기 때문 
            
- 의존성 역전 원칙을 지킬 수 있는 기술적인 요소
    - 어떤 변수에도 구상 클래스에 대한 래퍼런스를 저장하지 말자
        - new 연산자를 사용하면 구상 클래스에 대한 레퍼런스를 사용하게 되는 것이다
    - 구상 클래스에서 유도된 클래스를 만들지 말자
        - 구상 클래스에서 유도된 클래스를 만들면 특정 구상 클래스에 의존하게 된다
        - 인터페이스나 추상 클래스처럼 추상화된 것으로 부터 클래스를 만들어야 한다
    - 베이스 클래스에 이미 구현되어 있던 메소드를 오버라이드 하지 말자
        - 오버라이드 한다는 것은 애초부터 베이스 클래스가 제대로 추상화된 것이 아니었다고 볼 수 있다
        
        
### 패턴에 사용된 기술 포인트 ###
- 간단한 팩토리(Simple Factory)는 디자인 패턴이라고 할 수 없다. (문제 상황1 해결에 사용된 팩토리)
- New(객체생성) = 구상객체
    - 인터페이스에 맞춰서 코딩을하면 시스템에서 일어날 수 있는 여러 변화를 이겨낼 수 있다
      인터페이스를 바탕으로 코드를 만들면, 다형성 덕분에 어떤 클래스든 특정 인터페이스만 구현하면 사용할 수 있기 때문
    - 반대로 코드에서 구상 클래스를 많이 사용하면 새로운 구상 클래스가 추가될 때마다 코드를 고쳐야 하기 때문에 문제가 생길 수 있다
      즉 변화에 닫혀 있다
    - 결국, 새로운 구상 형식을 써서 확장해야 할 때 어떻게 해서든 다시 열 수 있어야 한다(열린 구조) 
- Simple Factory와의 차이점
    - 팩토리 메소드 패턴이 간단한 팩토리와 상당히 비슷하지만, simple factory는 일회용 처리방에 불과하지만,
      팩토리 메소드 패턴을 이용하면 어떤 구현을 사용할지를 서브클래스에서 결정하는 프레임워크를 만들 수 있다는 치가 있다

'''
