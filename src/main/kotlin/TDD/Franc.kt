package TDD

class Franc(
    amount: Int,
    currency: String
) : Money(amount = amount, currency = currency) {

    override fun times(multiplier: Int): Money {
        return Money.franc(amount * multiplier)
    }

    override fun currency(): String {
        return currency
    }
}