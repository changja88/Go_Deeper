package TDD

class Dollar(
    amount: Int,
    currecny: String
) : Money(amount = amount, currency = currecny) {

    override fun times(multiplier: Int): Money {
        return Money.dollar(amount * multiplier)
    }

    override fun currency(): String {
        return currency
    }
}

