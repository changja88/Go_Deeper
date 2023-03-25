package Casting

fun main(args: Array<String>) {
    val d = Drink()
    d.drink()

    //Up-Casting
    //washdishes 함수 호출 불가
    val b: Drink = Cola()
    b.drink()

    //b가 Cola와 호환되는지 확인
    //Down-Casting
    if (b is Cola) {
        // is : 변수가 자료형에 호환되는지를 체크한 후 변환해줌
        //중괄호 안에서만 Cola 함수 사용 가능
        b.washDishes()
    }

    val c = b as Cola
    c.washDishes()
    //as 사용시 반환 뿐만아니라 + 변수 자체도 Down-Casting 되기 때문에 에러 뜨지 않는다
    b.washDishes()
}

open class Drink {
    val name = "음료"

    //함수앞 open : override 가능
    open fun drink() {
        println("${name}를 마십니다")
        println("--------------------")
    }
}

class Cola : Drink() {
    val type = "콜라"

    override fun drink() {
        println("${name}중에 ${type}를 마십니다")
        println("--------------------")
    }

    fun washDishes() {
        println("${type}로 설거지를 합니다")
        println("--------------------")
    }
}