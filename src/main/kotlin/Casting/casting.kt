package Casting

fun main(args: Array<String>) {
    val earth1: Earth = Earth() //메모리에 Earth만 뜸.
//    val korea1: Korea = earth1 //다운캐스팅 불가능 왜냐하면 메모리에 Zigu만 있으니까!!

    val earth2: Earth = Korea() //메모리에 Earth, Asia, Korea 다 뜨고 포인터는 Zigu에 있음.
//    val korea2: Korea = earth2 //다운캐스팅 때 코틀린은 as를 사용해야함.
    val korea3: Korea = earth2 as Korea

    val korea4: Korea = Korea() //메모리에 Earth, Asia, Korea 다 뜨고 포인터는 Korea에 있음.
    val earth3: Earth = korea4 //업캐스팅시에는 as가 필요없음.

}


open class Earth {
}

open class Asia : Earth() {
}

class Korea : Asia() {
}