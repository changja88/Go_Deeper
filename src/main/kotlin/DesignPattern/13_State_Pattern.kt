/*
스테이트 패턴(State Pattern)

### 정의 ###
- 정의 : 객체의 내부 상태가 바뀜에 따라 객체의 행동을 바꿀 수 있따. 마치 객체의 클래스가 바뀌는 것과 같은 결과를 얻을 수 있다

### 목적 ###
- 변하는 부분을 캡슐화 한다

### 패턴에 사용된 기술 포인트 ###
- 상태를 별도의 클래스로 캡슐화한 다음 현재 상태를 나타내는 객체에게 행동을 위힘하기 때문에 내부 상태가 바뀜에 따라서 행동이 달라지게 된다
- "클래스가 바뀌는 것 같은" 클라이언트에서 사용하는 객체의 행동이 완전히 달라질 수 있다면 마치 그 객체가 다른 클래스로 부터 만들어진 객체처럼 느낀다
  실제로 다른 클래스로 변신하는 게 아니고 구성을 통해서 여러 상태 객체를 바꿔가면서 사용하기 때문에 이런 결과를 얻을 수 있다

- 상태전환을 구상객체에서 진행한다
    - 반드시 구상 객체에서 상태를 전환한 필요는 없다 context 객체에서 진행해도 된다
    - 하지만 상태 전환이 동적으로 결정되는 경우 구상객체에서 하는 것이 좋다 (의존성이 생기는 것을 방지)

- 구상상태클래스와 클라이언트가 직접 소통하는 일은 없어야 한다

- Strategy 패턴과의 차이점
    - 스테이트 패턴
        - 스테이트 패턴을 사용할 때는 상태 객체에 일련의 행동이 캡슐화된다
        - 상황에 따라 Context객체에서 여러 상태 객체 중 한 객체에게 모든 행동을 맡기게 된다
        - 객체의 내부 상태에 따라 현재 상태를 나타내는 객체가 바뀌게 되고, 그 결과로 컨텍스트 객체의 행동도 자연스럽게 바뀐다
        - 클라이언트는 상태 객체에 대해서 아무것도 몰라도 된다
        - 행동을 객체 내에 캡슐화 시키면 컨텍스트 내의 상태 객체를 바꾸는 것만으로도 컨텍스트 객체의 행동을 바꿀 수 있기 때문에
          컨텍스트 객체에게 수많은 조건문을 집어넣는 대신에 사용할 수 있는 패턴이다
    - 스트라테지 패턴
        - 스트라테지 패턴을 사용할 떄는 일반적으로 클라이언트에서 컨텍스트 객체한테 어떤 전략 객체를 사용할지를 지정해 준다
        - 스트라테지는 주로 실행시에 전략 객체를 변경할 수 있는 유연성을 제공하기 위한 용도로 쓰인다
        - 상속을 이용해서 클래스의 행동을 정의하다 보면 행동을 변경해야 할 때 마음대로 변경하기가 어렵기 때문에 일반적으로
          서브클래스를 만드는 대신 유연성을 극대화하기 위한 용도로 쓰인다

- 다른 패턴과의 차이점
    - 스테이트 패턴 -> 상태를 기반으로 하는 행동을 캐슐화하고 행동을 현재 상태한테 위임한다
    - 스트라테지 패턴 -> 알고리즘의 각 단게를 구현하는 방법을 서브클래스에서 구현한다
    - 템플릿 메소드 패턴 -> 바꿔 쓸 수 있는 행동을 캡슐화한 다음, 실제 행동은 다른 객체에 위임한다
*/
// ### 문제 상황 ###
// - 아래처럼 코드가 작성이 되어있었는데 변경 사항이 생겼다
class GumballMachine {
    val SOLD_OUT = 0
    val NO_QUARTER = 1
    val HAS_QUARTER = 2
    val SOLD = 3

    var state: Int = SOLD_OUT
    var count: Int = 0

    constructor(count: Int) {
        if (count > 0) state = NO_QUARTER
    }

    fun insertQuarter() {
        // 동전 투입시에 해야 할 일
        if (state == HAS_QUARTER) println("동전은 하나만 넣어주세요")
        else if (state == NO_QUARTER) println("동전을 넣으셨습니다")
        else if (state == SOLD_OUT) println("매진되었습니다")
        else if (state == SOLD) println("잠깐만 기다려주세요 알맹이가 나가고 있습니다")
    }

    fun ejectQuarter() {
        // 동전 반환시에 해야 할 일
        if (state == HAS_QUARTER) println("동전이 반환됩니다")
        else if (state == NO_QUARTER) println("동전을 넣어주세요")
        else if (state == SOLD_OUT) println("이미 알맹이를 뽑으셨습니다")
        else if (state == SOLD) println("동전을 넣지 않으셨습니다. 동전이 반환되지 않습니다")
    }

    fun turnCrank() {
        // 손잡이를 돌렸을 때 해야 할 일
    }

    fun dispense() {
        // 알맹이 배출시 해야할 일
    }
}

// ### 해결책 ###
// - 스테이트 패턴 도입
// - NoQuarterState, SoldOutState, .. 가 변하는 부분을 캡슐화하고 있다
interface State {
    fun insertQuarter()
    fun ejectQuarter()
    fun turnCrank()
    fun dispense()
}

class NoQuarterState(val gumballMachine: GumballMachine2) : State {
    override fun insertQuarter() {
        println("동전을 넣으셨습니다")
        //상태전환을 구상객체에서 진행한다
        gumballMachine.state = gumballMachine.hasQuarterState
    }

    override fun ejectQuarter() {
        println("동전을 넣어주세요")
    }

    override fun turnCrank() {
        println("동전을 넣어주세요")
    }

    override fun dispense() {
        println("동전을 넣어주세요")
    }
}

class SoldOutState(val gumballMachine: GumballMachine2) : State {
    override fun insertQuarter() {}
    override fun ejectQuarter() {}
    override fun turnCrank() {}
    override fun dispense() {}
}

class HasQuarterState(val gumballMachine: GumballMachine2) : State {
    override fun insertQuarter() {}
    override fun ejectQuarter() {}
    override fun turnCrank() {}
    override fun dispense() {}
}

class SoldState(val gumballMachine: GumballMachine2) : State {
    override fun insertQuarter() {}
    override fun ejectQuarter() {}
    override fun turnCrank() {}
    override fun dispense() {}
}

class GumballMachine2(val numberGumballs: Int) {
    val soldoutState: State
    val noQuarterState: State
    val hasQuarterState: State
    val soldState: State

    var count: Int = 0
    var state: State

    init {
        soldoutState = SoldOutState(this)
        noQuarterState = NoQuarterState(this)
        hasQuarterState = HasQuarterState(this)
        soldState = SoldState(this)

        this.count = numberGumballs
        if (numberGumballs > 0) state = noQuarterState
        else state = soldoutState
    }

    fun insertQuarter() {
        state.insertQuarter()
    }

    fun ejectQuarter() {
        state.ejectQuarter()
    }

    fun turnCrank() {
        this.turnCrank()
        state.dispense()
    }

    fun relaseBall() {
        println("나오고 있습니다")
        if (count != 0) count = count - 1
    }
}