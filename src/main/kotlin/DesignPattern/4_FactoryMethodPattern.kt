/*
팩토리 메소드 패턴(Factory Method Pattern)

### 정의 ###
- 팩토리 메소드 패턴에서는 객체를 생성하기 위한 인터페이스를 정의하는데, 어떤 클래스의 인스턴스를 만들지는 서브클래스에서 결정하게 만든다
  팩토리 메소드 패턴을 이용하면 클래스의 인스턴스를 만드는 일을 서브클래스에게 맡기는 것이다

### 목적 ###
- 모든 팩토리 패턴의 목적은 객체 생성의 캡슐화!
- 팩토리 메소드 패턴에서는 서브클래스에서 어떤 클래스를 만들지를 결정하게 함으로써 객체 생성을 캡슐화 한다

### 패턴에 사용된 기술 포인트 ###
- 간단한 팩토리(Simple Factory)는 디자인 패턴이라고 할 수 없다. (문제 상황1 해결에 사용된 팩토리)
- New(객체생성) = 구상객체
    - 인터페이스에 맞춰서 코딩을하면 시스템에서 일어날 수 있는 여러 변화를 이겨낼 수 있다
      인터페이스를 바탕으로 코드를 만들면, 다형성 덕분에 어떤 클래스든 특정 인터페이스만 구현하면 사용할 수 있기 때문
    - 반대로 코드에서 구상 클래스를 많이 사용하면 새로운 구상 클래스가 추가될 때마다 코드를 고쳐야 하기 때문에 문제가 생길 수 있다
      즉 변화에 닫혀 있다
    - 결국, 새로운 구상 형식을 써서 확장해야 할 때 어떻게 해서든 다시 열 수 있어야 한다(열린 구조)
- Simple Factory와의 차이점
    - 팩토리 메소드 패턴이 간단한 팩토리와 사당히 비슷하지만, simple factory는 일회용 처리방에 불과하지만,
      팩토리 메소드 패턴을 이용하면 어떤 구현을 사용할지를 서브클래스에서 결정하는 프레임워크를 만들 수 있다는 치가 있다
몇몇 포인트
- 어떤 변수에도 구상 클래스에 대한 래퍼런스를 저장하지 말자
    - new 연산자를 사용하면 구상 클래스에 대한 레퍼런스를 사용하게 되는 것이다
- 구상 클래스에서 유도된 클래스를 만들지 말자
    - 구상 클래스에서 유도된 클래스를 만들면 특정 구상 클래스에 의존하게 된다
    - 인터페이스나 추상 클래스처럼 추상화된 것으로 부터 클래스를 만들어야 한다
- 베이스 클래스에 이미 구현되어 있던 메소드를 오버라이드 하지 말자
    - 오버라이드 한다는 것은 애초부터 베이스 클래스가 제대로 추상화된 것이 아니었다고 볼 수 있다
*/

// ### 문제 상황(1) ###
// - 피자가 추가될 때마다 if문이 추가된다
fun odrerPizza(type: String): Pizza {
    var pizza: Pizza? = null
    if (type.equals("cheese")) pizza = CheesePizza()
    else if (type.equals("greek")) pizza = GreekPizza()
    else if (type.equals("pepperoni")) pizza = PepperoniPizza()
    else if (type.equals("greek")) pizza = GreekPizza()

    pizza!!.prepare()
    pizza!!.bake()
    pizza!!.box()
    return pizza
}

// ### 문제 상황(1) 해결책 ###
// - simple factory를 만든다
// - 바뀌지않는 부분을 남기고 변경되는 부분을 캡슐화 한다
class SimplePizzaFactory {
    fun createPizza(type: String): Pizza {
        var pizza: Pizza? = null
        if (type.equals("cheese")) pizza = CheesePizza()
        else if (type.equals("pepperoni")) pizza = PepperoniPizza()
        else if (type.equals("greek")) pizza = GreekPizza()
        else if (type.equals("clam")) pizza = ClamPizza() // 추가
        else if (type.equals("veggie")) pizza = VeggiePizza() // 추가

        return pizza!!
    }
}

class PizzaStore(val factory: SimplePizzaFactory) {
    fun orderPizza(type: String): Pizza {
        // New 연산자 대신에 팩토리 사용(구상 클래스의 인스턴스를 만들 필요가 없음)
        // PizzaStore 안에 createPizza와 같은 메소드로 캡슐화를 시키지 않는 이유
        // - 이렇게 하며되면 어잿든 PizzaStore클래스는 Pizza클래스라는 구상 클래스를 직접 만들게 됨
        val pizza: Pizza = factory.createPizza(type)
        pizza.prepare()
        pizza.bake()
        pizza.box()
        return pizza
    }
}
// ### 문제 상황(2) ###
// - 피자집에 분점이 생기기 시작했고, 분점마다 고유의 피자 스타일이 생겼다
// - 문제상황(1) 해결책을 적용하면 NYPizzaFactory, ChicagoPizzaFactory ...등등을 계속 만들어야 한다

// ### 문제 상황(2) 해결책 ###
// - 피자 객체를 생성을 AbstractPizzaStore에게 맡기고, 각 분점은 AbstractPizzaStore을 상속해서 구체피자를 만든다
// - 구상 클래스의 인스턴스를 만드는 일을 한 객체에서 전부 처리하는 방식에서 일련의 서브클래스에서 처리하는 방식으로 변경
//      - 구상 클래스의 인스턴스 : 피자, 한 객체 : Factory, 서브클래스 : NYPizzaStore
// - 장점
//      - 팩토리 메소드를 이용하면 객체를 생성하는 작업을 서브클래스에 캡슐화시킬 수 있다
//      - 슈퍼 클래스에 있는 클라이언트 코드와 서브클래스에 있는 객체 생성코드를 분리시킬 수 있다
//      - 슈퍼 클래스는 실제로 생성된 구상 객체가 무엇인지 알 수 없게 만든다
abstract class AbstractPizzaStore {
    fun orderPizza(type: String): Pizza {
        // 피자 객체를 가지고 여러가지 작업을 하지만 피자는 추상 클래스이기 때문에 실제로 어떤 구상 클래스에서
        // 작업이 처리되는지 알 수 없다 (피자와 피자스토어는 분리 되어 있다)
        val pizza = createPizza(type) // 펙토리 객체가 아닌 클래스 매소드를 호출한다
        pizza.prepare()
        pizza.bake()
        pizza.box()

        return pizza
    }

    //팩토리 메소드가 추상 메소드로 변경되었다 (추상 팩토리 메소드)
    abstract fun createPizza(type: String): Pizza
}

class NYPizzaStore : AbstractPizzaStore() {
    // PizzaStore를 상속 받은 분점들이 자기 스타일의 피자를 만들수 있게 되었다
    override fun createPizza(type: String): Pizza {
        var pizza: Pizza? = null
        if (type.equals("cheese")) pizza = NYCheesePizza()
        else if (type.equals("pepperoni")) pizza = NYPepperoniPizza()
        else if (type.equals("greek")) pizza = NYGreekPizza()
        else if (type.equals("clam")) pizza = NYClamPizza() // 추가
        else if (type.equals("veggie")) pizza = NYVeggiePizza() // 추가
        return pizza!!
    }
}

fun main() {
    val nyPizzaStore = NYPizzaStore()
    nyPizzaStore.orderPizza("cheese")
}





