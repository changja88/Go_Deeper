package TDD

import java.util.Currency

abstract class Money(
    protected val amount: Int,
    protected val currency: String
) {

    companion object {
        fun dollar(amount: Int): Dollar {
            return Dollar(amount, "USD")
        }

        fun franc(amount: Int): Franc {
            return Franc(amount, "CHF")
        }
    }

    override fun equals(other: Any?): Boolean {
        val money: Money = other as Money
        return javaClass.equals(money.javaClass) && money.amount == amount
    }

    abstract fun times(multiplier: Int): Money
    abstract fun currency(): String
}