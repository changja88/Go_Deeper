open class Dough {}
open class Sauce {}
open class Cheese {}
open class Veggie {}
open class Pepperoni {}
open class Clam {}
class ThinCrustDough : Dough() {}
class MarinaraSauce : Sauce() {}
class ReggianoCheese : Cheese() {}
class Garlic : Veggie() {}
class Onion : Veggie() {}
class Mushroom : Veggie() {}
class RedPepper : Veggie() {}
class SlicedPepperoni : Pepperoni() {}
class FreshClams : Clam() {}
interface Pizza {
    fun prepare() {}
    fun bake() {}
    fun box() {}
}

class CheesePizza() : Pizza {}
class GreekPizza() : Pizza {}
class PepperoniPizza() : Pizza {}
class ClamPizza() : Pizza {}
class VeggiePizza() : Pizza {}
class NYCheesePizza() : Pizza {}
class NYPepperoniPizza() : Pizza {}
class NYGreekPizza() : Pizza {}
class NYClamPizza() : Pizza {}
class NYVeggiePizza() : Pizza {}
class Amplifier()
class Tuner()
class DvdPlayer()
class Projector()
class TheaterLights()
class Screen()
class PopcornPopper()
class Engine() {
    fun start() {}
}

class Key() {
    fun turns(): Boolean {
        return true
    }
}

class Doors() {
    fun lock() {}
}