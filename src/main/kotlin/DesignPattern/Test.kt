open abstract class Cat() {
    abstract fun attack()
}

class Tiger() : Cat() {
    override fun attack() {
        println("jump")
    }
}


fun main() {
    val tiger: Cat = Tiger()
    tiger.attack()
}