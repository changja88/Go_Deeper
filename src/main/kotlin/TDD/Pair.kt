package TDD

class Pair(val from: String, val to: String) {
    override fun equals(other: Any?): Boolean {
        val pair: Pair = other as Pair
        return (from.equals(pair.from) && to.equals(pair.to))
    }

    override fun hashCode(): Int {
        return 0
    }
}