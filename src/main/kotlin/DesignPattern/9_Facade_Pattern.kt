/*
퍼사드 패턴(Facade Pattern)
### 정의 ###
- facade : 겉모양, 외관
- 어떤 서브시스템의 일련의 인터페이스에 대한 통합된 인터페이스를 제공한다.
  퍼사드에서 고수준 인터페이스를 정의하기 때문에 서브시스템을 쉽게 사용할 수 있다

### 목적 ###
- 사용하기 쉬운 인터페이스를 제공함과동시에 클라이언트와 구성요소들로 이루어진 서브시스템을 분리시킨다

- 디자인 원칙 : (최소 지식 원칙, 데메테르의 법칙) 정말 친한 친구하고만 얘기하라
    - 어떤 객체든 그 객체와 상호작용을 하는 클래스의 개수에 주의해야 하며, 그런 객체들과 어떤 식으로 상호작용을 하는지도 주의를 기울여야 한다
    - 복잡하게 얽혀서 시스템의 한 부분을 변경했을 때 다른 부분까지 줄줄이 고쳐야 되는 상황을 미리 방지할 수 있다
- 객체 관계를 생성하는 가이드 라인 (아래 코드로 구체 사례 확인)
    - 아래에 해당하는 객체의 메소드만 호출하라
        - 객체 자체
        - 메소드에 매개변수로 전달된 객체
        - 그 메소드에서 생성하거나 인스턴스를 만든 객체
        - 그 객체에 속하는 구성요소

### 패턴에 사용된 기술 포인트 ###
-퍼사드 패턴을 사용하면 클라이언트 구현과 서브시스템을 분리시킬 수 있다
    - 회사에서 씨어터 시스템을 업그레이드 하기로 한경우 인터페이스가 크게 달라질텐데,
      클라이언트가 퍼사드를 사용하고 있다면 클라이언트 코드는 수정할 필요가 없다

### 문제 상황 ###
- 영화를 보기 위해서 너무 많은 단계를 거쳐야 한다
fun watchMovie() {
    popper.on()
    lights.dim()
    screen.down()
    projector.on()
    dvd.on()
    // 줄줄이 엄청 많음
}

### 해결책 ###
- 파사드 패턴을 도입한다
*/
class HomeTheaterFacade(
    // 구성 부분, 사용하고자 하는 서브시스템의 모든 구성요소들이 인스턴스 변수 형태로 저장된다
    val amp: Amplifier,
    val tuner: Tuner,
    val dvd: DvdPlayer,
    val projector: Projector,
    val lights: TheaterLights,
    val screen: Screen,
    val popper: PopcornPopper
) {
    fun watchMovie() {
        // 위 구성요소들을 사용하여 기능 구현
    }
}


// ### 호출 가능한 객체의 메소드 사례 ###
// 원칙을 따리지 않는 경우
//fun getTemp() {
    // station으로부터 thermometer라는 객체를 받은 다음, 그 객체의 메소드를 직접 호출 한다
//    val thermometer: Thermometer = station.getThermometer()
//    return thermometer.getTemperature()
//}

// 원칙을 따르는 경우
//fun getTemp() {
    // 최소 지식 원칙을 적용하여 station클래스에 thermometer에 요청 해주는 메소드를 추가했다
//    return station.getTemperature()
//}

//상세 예시
class Car(
    val engine: Engine // 클래스의 구성요소 -> 이 구성요소의 메소드는 호출 해도 된다
) {
    fun start(key: Key) { // 매개변수로 전달된 객체의 메소드는 호출 해도 된다
        val doors: Doors = Doors() // 새로운 객체 생성, 이 객체의 메소드는 호출해도 된다

        val authorized: Boolean = key.turns()

        if (authorized) {
            engine.start() // 클래스 구성 요소 -> 호출 가능
            updateDashboardDisplay() // 객체 내에 있는 메소드 -> 호출 가능
            doors.lock() // 직접 만든 객체 -> 호출 가능
        }
    }

    fun updateDashboardDisplay() {

    }
}

