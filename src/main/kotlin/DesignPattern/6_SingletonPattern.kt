/*
싱글턴 패턴(Single Pattern)
### 정의 ###
정의: 싱글턴 패턴은 해당 클래스의 인스턴스가 하나만 만들어지고, 어디서든지 그 인스턴스에 접근할 수 있도록 하기 위한 패턴입니다

### 목적 ###
- 클래스 인스턴스가 하나만 만들어지도록 하고, 그 인스턴스에 대한 전역 접근을 제공한다

### 패턴에 사용된 기술 포인트 ###
전역변수의 단점
- 전역변수는 사용을 하던 하지 않던 언제나 자원을 사용한다
- 전역변수를 사용하게 되면 네임스페이스가 더려워 진다

생성자
- 싱글턴에는 public으로 설정된 생성자가 없다
- 객체가 필요할 때는 인스턴스를 직접 만드는게 아니고, 인스턴스를 달라고 요청을 해야 한다 (getInstance)
- getInstance는 최초 요청시에 객체를 생성하기 때문에 레이지 생성이다

상속
- 싱글턴으로 구현된 클래스는 서브클래스를 만들수가 없다
  private으로 지정된 생성자를 가진 클래스는 확장할 수 없기 때문에 생성자를 변경해야 서브클래스를 만들수 있다
  하지만 생성자가 private이 아니면 싱글턴이 아니게된다
*/

//고전적인 싱글턴 패턴 구현 방법
class Singleton private constructor() {
    companion object {
        // 코틀린에서는 static이 companion object이다
        // const
        // - 상수 선언에 사용된다
        // - val과 const의 차이점은 val은 불변이지만 프로그램이 수행중에 결정된다 (val a = b +c) 하지만 const는 프로그램 시작과 동시에 정해진다
        var uniqueInstance: Singleton? = null
        fun getInstance(): Singleton {
            if (uniqueInstance == null) {
                uniqueInstance = Singleton()
            }
            return uniqueInstance!!
        }
    }
}

// ### 문제 상황(1) ###
// - Singleton2의 경우 서로 다른 쓰레드에서 최초로 getInstance를 호출 했을 경우 두개의 객체 생성이 가능하다
class Singleton2 private constructor() {
    companion object {
        var uniqueInstance: Singleton2? = null
        fun getInstance(): Singleton2 {
            if (uniqueInstance == null) uniqueInstance = Singleton2()
            return uniqueInstance!!
        }
    }
}

// ### 문제 상황(1) 해결책 ###
// - 동기화를 시켜서 멀티쓰레딩 문제를 해결 해야 한다
// - Synchronized를 사용하게되면 한 스레드가 메소드 사용을 끝내기 전까지 다른 스레드는 기다려야 한다
class Singleton3 private constructor() {
    companion object {
        var uniqueInstance: Singleton3? = null

        @Synchronized
        fun getInstance(): Singleton3 {
            if (uniqueInstance == null) uniqueInstance = Singleton3()
            return uniqueInstance!!
        }
    }
}
// ### 문제 상황(2) ###
// - 1번문제의 해결책은 새로운 문제를 만든다
// - 동기화를 시키게되면 속도에 문제가 발생한다
//   uniqueInstance 변수에 싱글턴 인스턴스를 대입하고 나면 굳이 이 메소드를 동기화된 상태로 유지시킬 필요가 없다

// ### 문제 상황(2) 해결책 ###
// - 1번> getInstance의 속도가 중요하지 않다면 1번 해결책을 유지한다
// - 2번> 인스턴스를 필요할때 생성하지 말고, 처음부터 만들어 버린다
// - 3번> DCL(Double-checking Locking)을 써써 getInstance()에서 동기화되는 부분을 줄인다
//   인스턴스가 생성되어 있는지 확인한 다음, 생성되어 있지 않을 때만 동기화를 할 수 있다

// 3번 적용
class Singleton4 private constructor() {


    companion object {
        @Volatile // 멀티쓰레딩을 쓰더라도 uniqueinstance변수가 singleton인스턴스로 초기화되는 과정이 올바르게 진행된다
        var uniqueInstance: Singleton4? = null

        fun getInstance(): Singleton4? {
            if (uniqueInstance == null) {
                synchronized(Singleton4::class.java) { // 인스턴스가 없는 경우에만 동기화를 진행한다
                    if (uniqueInstance == null) uniqueInstance = Singleton4()
                }
            }
            return uniqueInstance
        }
    }
}
