fun main(args: Array<String>) {
    println("Hello World!")

    // Try adding program arguments via Run/Debug configuration.
    // Learn more about running applications: https://www.jetbrains.com/help/idea/running-applications.html.
    println("Program arguments: ${args.joinToString()}")

    val number: Int? = 10
    var test: String = "안녕하세요"

    arrayWithString.forEach {
        println(it)
    }
    println(sum_as_text(1, 2))

    for (i in 1..10) {
        println("" + i + "번째 반복 입니다 ")
    }
    val listWithString = mutableListOf<String>("안", "녕", "하", "세", "요")
    pringGuGuDan(20, 2)
}


fun sum_as_text(number1: Int, number2: Int): String {
    val result = number1 + number2
    val resultText = "정답은 " + result + " 입니다"
    return resultText
}

var arrayWithInt = arrayOf<Int>(1, 2, 3, 4, 5)
var arrayWithString = Array(5, { "value" })


fun pringGuGuDan(fromX: Int, toY: Int) {
    if (fromX or toY > 9) {
        println("9단 까지만 출력이 가능합니다")
        return
    }
    if (toY < fromX) {
        println("입력을 확인해주세요")
        return
    }


    for (dan in fromX..toY) {
        for (i in 1..9) {
            println("" + dan + " x " + i + " = " + dan * i)
        }
    }
}
