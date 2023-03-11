import java.lang.System
import java.util.Scanner

fun main(args: Array<String>) {
    println("Hello World!")

    // Try adding program arguments via Run/Debug configuration.
    // Learn more about running applications: https://www.jetbrains.com/help/idea/running-applications.html.
    println("Program arguments: ${args.joinToString()}")
}


class Caculater2 constructor(initialNum: Int = 0) {
    var result: Int = 10
        set(value) {
            field = value
        }

    init {
        this.result = initialNum
    }
    fun calculater(operater:Char, num: Int){

    }
}