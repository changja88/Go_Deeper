package TDD

import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test

class Test {

    @Test
    fun testMultiplication() {
//        val five: Dollar = Money.dollar(5)
//        assertEquals(Dollar(10), five.times(2))
//        assertEquals(Dollar(15), five.times(3))
    }

    @Test
    fun testEquality() {
        assertTrue(Money.dollar(5) == Money.dollar(5))
        assertFalse(Money.dollar(5) == Money.dollar(6))
//        assertTrue(Franc(5) == Franc(5))
//        assertFalse(Franc(5) == Franc(6))
//        assertFalse(Franc(5).equals(Money.dollar(5)))
    }

    @Test
    fun testCurrency() {
        assertEquals("USD", Money.dollar(1).currency())
        assertEquals("CHF", Money.franc(1).currency())
    }
}
