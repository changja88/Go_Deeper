/*
커맨드 패턴(Command Pattern)
### 정의 ###
정의 : 커맨드 패턴을 이용하면 요구 사항을 객체로 캡슐화 할 수 있으며, 매개변수를 써서 여러 가지 다른 요구 사항을 집어넣을 수도 있다
      또한 요청 내역을 큐에 저장하거나 로그로 기록할 수도 있으며, 작업취소 기능도 지원한다

### 목적 ###
- 요청을 하는 객체와 그 요청을 수행하는 객체를 분리 시킨다 (메소드 호출 캡슐화)
  계산하는 코드를 호출한 객체에서는 어떤 식으로 일을 처리해야 하는지에 대해 전형 신경쓰지 않아도 된다
- 활용성
    - 1> 커맨드를 묶어서 사용하게 되면 메크로 커맨드 패턴이 된다 (불 켜고, TV켜고, 영화 틀고)
    - 2> 요청을 큐에 저장 할 수 있다
        - 큐 한쪽 끝은 커맨드를 추가할 수있도록 하고, 다른 쪽 끝에는 커맨드를 처리하기 위한 스레드를 만든다
          스레드에서는 우선 excute() 메소드를 호출하고 그 호출이 완료되고 나면 커맨드 객체를 버리고 새로운 커맨드 객체를 가져온다
    - 3> 로그 찍기 
        - 모든 행동을 기록했다가 앱이 죽은 경우 실행된 행동들을 다시 호출해서 복구 한다
        - store(), load() 메소드를 추가한다
          커맨드가 실행이 될 때마다 디스크에 store함수를 통해서 저장한다
          시스템이 죽은 경우 load함수를 통해서 작업을 다시 불러와서 진행한다

### 패턴에 사용된 기술 포인트 ###
인보커, 리시버, 커맨드 객체 3가지 조합으로 사용된다
    - 인보커 -> 커맨드 객체를 실행 시킨다 (클라이언트가 사용하는 리모컨)
    - 커맨드 객체 -> 리시버를 동작 시킨다 (조명을 켜라는 명령)
    - 리시버 -> 실제 기능을 가지고 있다 (조명을 켜라는 명령을 실제로 수행하는 객체)
사용 순서
    - 사전 준비
        - 1> 인보커를 만든다 (리모컨, remote)
        - 2> 리시버를 만든다 (조명, light)
        - 3> 리시버를 인자로 넘겨서 커맨드 객체를 만든다 (불켜명령, lightOnCommand)
        - 4> 인보커에 커맨드를 등록 시킨다
    - 실행
        - 인보커가 커맨드 객체를 실행 시킨다 (buttonWasPressed)
        - 커맨드 객체가 리시버를 실행 시킨다 (excute)
        - 리시버가 일을 한다 (on)
NoCommand활용
- NoCommand는 일종의 null객체이다
- 클라이언트 쪽에서 null을 처리하지 않아도 되도록 하고 싶을때 활용 할 수 있다
- 리모컨에 아무런 기능이 할당되어 있지 않은 경우 NoCommand로 채워서 null을 처리하지 않게 할 수도 있다
- null객체도 일종의 디자인패턴으로 분류하기도 한다

### 문제 상황 ###

*/
// 리시버 객체
class Light() {
    fun on() {}
    fun off() {}
}

interface Command {
    fun excute()
}

// 커맨드 객체
class LightOnCommand(val light: Light) : Command {
    override fun excute() {
        light.on()
    }

    fun undo() {
        light.off()
    }
}

// 인보커 객체
class SimpleRemoteControl() {
    var slot: Command? = null

    fun setCommand(command: Command) {
        slot = command
    }

    fun buttonWasPressed() {
        slot!!.excute()
    }
}


fun main() { // main 함수가 커맨드패턴에서 클라이언트에 해당 하는 부분
    //remote 변수가 인보커 역할을 한다. 필요한 작업을 요청할 때 사용할 커맨드 객체를 인자로 전달 받는다
    val remote: SimpleRemoteControl = SimpleRemoteControl()
    // 요청을 받아서 처리할 리시버인 light객체를 생성한다
    val light: Light = Light()
    // 커맨드 객체를 생성하면서 리시버를 전달해준다
    val lightOn: LightOnCommand = LightOnCommand(light)
    // 커맨드 객체를 인보커에게 전달한다
    remote.setCommand(lightOn)

    remote.buttonWasPressed()
}

