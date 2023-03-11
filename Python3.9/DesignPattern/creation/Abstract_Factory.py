from abc import ABC, abstractmethod

from DesignPattern.creation.Factory_Method import PizzaStore
from DesignPattern.trash import *

################################################################
# Factory_Method 패턴에 이어서 보는게 좋음
'''
지역별로 다른 종류의 피자를 생성해야 한다 -> 지역별 피자 원재료를 관리하면 되지 않을까?
- 추상 클래스 PizzaIngredientFactory를 만들고 각각 지역별로 상속받아서 원재료를 관리하면 될까?
'''


class PizzaIngredientFactory(metaclass=ABC):
    @abstractmethod
    def createDough(self) -> Dough:
        pass

    @abstractmethod
    def createSauce(self) -> Sauce:
        pass

    @abstractmethod
    def createCheese(self) -> Cheese:
        pass

    @abstractmethod
    def createVeggis(self) -> list[Veggie]:
        pass

    @abstractmethod
    def createPepperoni(self) -> Pepperoni:
        pass

    @abstractmethod
    def createClam(self) -> Clam:
        pass


class NYPizzaIngredientFactory(PizzaIngredientFactory):

    def createDough(self) -> Dough:
        return ThinCrustDough()

    def createSauce(self) -> Sauce:
        return MarinaraSauce()

    def createCheese(self) -> Cheese:
        return ReggianoCheese()

    def createVeggis(self) -> list[Veggie]:
        return [Garlic(), Onion(), Mushroom(), RedPepper()]

    def createPepperoni(self) -> Pepperoni:
        return SlicedPepperoni()

    def createClam(self) -> Clam:
        return FreshClams()


class Pizza(metaclass=ABC):
    @abstractmethod
    def prepare(self): pass

    def bake(self):
        print("bake for 25min at 350")

    def cut(self):
        print("cutting the pizza into diagonal slices")

    def box(self):
        print("place pizza in official pizzasotre box")


class CheesePizza(Pizza):
    def __init__(self, ingredient_factory: PizzaIngredientFactory):
        self.ingredient_factory = ingredient_factory

    def prepare(self):
        self.dough = self.ingredient_factory.createDough()
        self.sauce = self.ingredient_factory.createSauce()
        self.cheese = self.ingredient_factory.createCheese()


class PeperoniPizza(Pizza):
    def __init__(self, ingredient_factory: PizzaIngredientFactory):
        self.ingredient_factory = ingredient_factory

    def prepare(self):
        self.dough = self.ingredient_factory.createDough()
        self.sauce = self.ingredient_factory.createSauce()
        self.cheese = self.ingredient_factory.createCheese()


class NYPizzaStore(PizzaStore):
    def create_pizza(self, type: str) -> Pizza:
        pizza = None
        ingredient_factory: PizzaIngredientFactory = NYPizzaIngredientFactory()
        # 상속보다는 구성을 사용하고 있음
        # 추상 팩토리 패턴에서는 인터페이스를 이용하여 서로 연관된, 또는 의존하는 객체를 구상 클래스를 지정하지 않고도 생성할 수 있다
        # - 타입이 NYPizzaIngredientFactory이 아니다!

        if type == 'cheese':
            pizza = CheesePizza(ingredient_factory=ingredient_factory)
        elif type == 'peperoni':
            pizza = PeperoniPizza(ingredient_factory=ingredient_factory)

        return pizza


'''
- Factory Method 패턴과는 어떤 차이점이 있을까?
    - Abstract Factory, Factory Method 두 패턴 모두 목적인 지역별로 다르게 생산되는 피자를 관리하는 것이다
    - Factory Method -> 지역별 PizzaStore를 만들어서 지역별 피자 생성을 가능 하도록 만듬
    - Abstract Factory -> 지역별 PizzaStore에 원재로팩토리를 다르게 넣어줘서 지역별 다른 피자를 생성을 가능 하도록 만듬
      
- Factory_Mehtod 파일 처음에 나오는 order_pizza랑 거의 같은데?
    - 둘다 pizza라는 추상화된 것에 의존하고 있기 때문에 문제가 없다!
    - 둘다 변화는 것을 캡슐화하는 방법이 다를뿐이다!
'''
################################################################
'''
총정리

추상 팩토리 패턴 (Abstract Factory Pattern)
### 정의 ###
정의 : 추상 팩토리 패턴에서는 인터페이스를 이용하여 서로 연관된, 또는 의존하는 객체를 구상 클래스를 지정하지 않고도 생성할 수 있다

### 목적 ###
- 구상 클래스에 직접 의존하지 않고도 서로 관련된 객체들로 이루어진 제품군을 만들기 위한 용도로 쓰인다
- 의존성 뒤집기 원칙을 따르면 구상 형식에 대한 의존을 피하고 추상화를 지향할 수 있다

### 패턴에 사용된 기술 포인트 ###
- 구성(compistion)을 사용해서 어떤 클래스의 인스턴스를 만들지 결정한다
'''
################################################################
