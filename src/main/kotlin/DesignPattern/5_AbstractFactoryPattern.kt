/*
추상 팩토리 패턴 (Abstract Factory Pattern)
### 정의 ###
정의 : 추상 팩토리 패턴에서는 인터페이스를 이용하여 서로 연관된, 또는 의존하는 객체를 구상 클래스를 지정하지 않고도 생성할 수 있다

### 목적 ###
- 구상 클래스에 직접 의존하지 않고도 서로 관련된 객체들로 이루어진 제품군을 만들기 위한 용도로 쓰인다
- 의존성 뒤집기 원칙을 따르면 구상 형식에 대한 의존을 피하고 추상화를 지향할 수 있다

### 패턴에 사용된 기술 포인트 ###
- 구성(compistion)을 사용해서 어떤 클래스의 인스턴스를 만들지 결정한다
*/

//### 문제 상황(1) ###
//- 피자 원재료를 관리할 필요성이 생겼다
//- 시카고, 뉴욕, 켈리포니아 마다 원재료군이 다르다

//### 문제 상황(1) 해결책 ###
//- 추상 팩토리를 도입해서 서로 다른 피자에서 필요로 하는 원재료군을 생산한다
//- 추상 팩토리를 통해서 제품군을 생성하기 위한 인터페이스를 제공할 수 있다
//  이 인터페이스를 이용하는 코드를 만들면 코드를 제품을 생산하는 실제 팩토리와 분리시킬 수 있다
interface PizzaIngredientFactory {
    fun createDough(): Dough
    fun createSauce(): Sauce
    fun createCheese(): Cheese
    fun createVeggis(): List<Veggie>
    fun createPepperoni(): Pepperoni
    fun createClam(): Clam
}

class ChicagePizzaIngredientFactory : PizzaIngredientFactory {
    override fun createDough(): Dough {
        return ThinCrustDough()
    }

    override fun createSauce(): Sauce {
        return MarinaraSauce()
    }

    override fun createCheese(): Cheese {
        return ReggianoCheese()
    }

    override fun createVeggis(): List<Veggie> {
        val veggies = listOf<Veggie>(Garlic(), Onion(), Mushroom(), RedPepper())
        return veggies
    }

    override fun createPepperoni(): Pepperoni {
        return SlicedPepperoni()
    }

    override fun createClam(): Clam {
        return FreshClams()
    }
}

abstract class Pizza2 {
    var name: String? = null
    var dough: Dough? = null
    var sauce: Sauce? = null
    var veggies: List<Veggie>? = null
    var cheese: Cheese? = null
    var pepperoni: Pepperoni? = null
    var clam: Clam? = null

    abstract fun prepare()
    fun bake() {
        println("bake for 25min at 350")
    }

    fun cut() {
        println("cutting the pizza into diagonal slices")
    }

    fun box() {
        println("place pizza in official pizzasotre box")
    }

    override fun toString(): String {
        return name!!
    }
}

class CheesePizza2(val ingredientFactory: PizzaIngredientFactory) : Pizza2() {
    override fun prepare() {
        val dough = ingredientFactory.createDough()
        val sauce = ingredientFactory.createSauce()
        val cheese = ingredientFactory.createCheese()
    }
}

class VeggiePizza2(val ingredientFactory: PizzaIngredientFactory) : Pizza2() {
    override fun prepare() {
        val dough = ingredientFactory.createDough()
        val sauce = ingredientFactory.createSauce()
        val cheese = ingredientFactory.createCheese()
    }
}

class ChicagoPizzaStore {
    fun createPizza(type: String): Pizza2 {
        val ingredientFactory: PizzaIngredientFactory = ChicagePizzaIngredientFactory()
        // 원재료 팩토리만 바꿔주면 시카고풍 피자, 뉴욕풍 피자 전부다 만들 수 있다

        var pizza: Pizza2? = null
        if (type.equals("cheese")) {
            pizza = CheesePizza2(ingredientFactory)
        } else if (type.equals("veggie")) {
            pizza = VeggiePizza2(ingredientFactory)
        }
        return pizza!!
    }
}

fun main() {
    ChicagoPizzaStore().createPizza("cheese")
}