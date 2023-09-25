/*
어답터 패턴(Adapter Pattern)
### 정의 ###
- 한 클래스의 인터페이스를 클라이언트에서 사용하고자 하는 다른 인터페이스로 변환한다

### 목적 ###
- 어답터를 이용하면 인터페이스 호환성 문제 때문에 같이 쓸 수 없는 클래스들을 연결해서 쓸 수 있다

### 패턴에 사용된 기술 포인트 ###
- 인터페이스를 변환해주는 어답터를 만들면 클라이언트와 구현된 인터페이스를 분리시킬수 있고, 나중에 인터페이스가 바뀌더라고 그 변경 내역은 어답터에 캡슐화 된다
- 어답티를 새로 바뀐 인터페이스로 감쌀 때는 구성(composition)을 사용한다
- 클라이언트를 특정 구현이 아닌 인터페이스에 연결 시킨다
- 어답터는 클래스 어답터(상속 사용), 객체 어답터(구성 사용) 두종류가 있지만, 클래스 어답터의 경우에는 다중 상속이 필요하기때문에 쓰이지 않는다

### 유사패턴과의 차이 ###
- 데코레이터 : 인터페이스는 바꾸지 않고 책임(기능)만 추가
- 어답터 : 한 인터페이스를 다른 인터페이스로 변환
- 퍼사드 : 인터페이스를 간단하게 바꿈

### 문제 상황 ###
- Duck 클래스를 사용하고 있었는데 종류가 다른 Turkey 클래스를 같이 써야할 일이 발생했다
- Duck 인터페이스와 Turkey 인터페이스가 다르기 때문에 바로 같이 사용할 수 없다

### 해결책 ###
- Adapter를 만든다

*/
interface Duck2 {
    fun quack()
    fun fly()
}

class MallardDuck2 : Duck2 {
    override fun quack() {
    }

    override fun fly() {
    }
}

interface Turkey {
    fun gobble()
    fun fly()
}

class WildTurkey : Turkey {
    override fun gobble() {
        println("gobble")
    }

    override fun fly() {
        println("fly")
    }
}

class TurkeyAdapter(
    val turkey: Turkey // 중요 포인트! -> 구성을 사용하고 있다
) : Duck2 {

    override fun quack() {
        turkey.gobble()
    }

    override fun fly() {
        turkey.fly()
    }
}

fun main() {
    val duck: MallardDuck = MallardDuck()
    val turkey: WildTurkey = WildTurkey()
    val turkeyAdapter: TurkeyAdapter = TurkeyAdapter(turkey)

    turkey.gobble()
    turkey.fly()


    fun testDuck(duck: Duck2) {
        // 여기가 중요하다 Duck을 받는 자리에 turkey를 넣어 줄 수 있다!
        duck.quack() // 최종적으로 turkey를 duck처럼 사용할 수 있다!
        duck.fly()
    }

    testDuck(turkeyAdapter)
}