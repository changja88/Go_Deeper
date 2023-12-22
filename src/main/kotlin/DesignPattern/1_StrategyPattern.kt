/*
Strategy Pattern
### 정의 ###
- 스트래티지 패턴(Strategy Pattern)
    - 아래 예제가 스트래티지 패턴이다
    - 알고리즘군을 정의하고 각각을 캡슐화하여 교환해서 사용할 수 있도록 만든다
    - 스트래티지를 활용하면 알고리즘을 사용하는 클러이언트와는 독립적으로 알고리즘을 변경할 수 있다

### 목적 ###
- 디자인 원칙 : 애플리케이션에서 달라지는 부분을 찾아내고, 달라지지 않는 부분으로부터 분리 시킨다

### 패턴에 사용된 기술 포인트 ###
- 캡슐화해서 "교환"을 할 수 있는 이유가 중요하다 (스트래티지 패턴이 가능해지는 이유)
- 아래 해결책 캡슐화 구현 방법을 적용했기 때문에 교환이 가능하다
    - 변수를 선언할 때는 보통 추상 클래스나 인터페이스 같은 상위 형식으로 선언했기 때문
      ex) FlyWithWings(구체 클래스)로 변수를 선언한게 아니라 FlyBehavior(인터페이스)로 선언을 했기 때문에 교환이 가능하다
    - FlyWithWings를 또다른 구체 클래스 FlayNoWay로 교환이 가능하다 (스트래티지 패턴이 가능해짐)
- 상속보다는 구성(Composition)이 좋을 수 있다
    - A는 B이다 보다 A에는 B가 있다 가 더 좋을 수 있다
        - 각 오리에는 FlyBehavior와 QuackBehavior가 상속으로 부터 받은게 아니다 (상속 아님)
        - 각 오리에는 FlyBehavior 와 QuackBehavior가 있으며, 각각 행동을 위임 받는다 (구성이다)
    - 이런 방식을 구성(Composition)이라고 한다

### 문제상황 ###
Duck이라는 슈퍼 클래스를 만들었다
1. 다른 duck 클래스들이 위 슈퍼클래스를 상속 받고 있다
2. duck 슈퍼클래스에 fly 기능을 추가 하였다
3. duck 슈퍼클래스를 상속 받은 모든 서브 클래스들이 fly 기능을 갖게 되었다
4. 문제 발생 -> 모든 서브 클래스 들이 fly 기능을 갖아서는 안된다 (고무 오리는 날지 못한다)
5. 상속을 활용한 임시 해결책 : fly 기능을 할 수 없는 서브 클래스에서는 fly를 오버라이드 하여 못 날게 한다

위 처럼 문제를 해결 했을 때의 문제점
1. 서브 클래스에서 코드가 중복된다
3. 모든 오리의 행동을 알기가 어렵다
4. 슈퍼클래스를 변경 했을 때 다른 오리들한테 원치 않은 영향을 줄 수 있다

### 해결책 ###
캡슐화
1. 캡슐화대상 선택 -> 달라지는 부분을 찾아내고, 달라지지 않는 부분으로부터 분리 시킨다
    - 오리들의 행동을 duck 클래스에서 뽑아 낸다
    - fly, quack만 오리들마다 달라지는 행동이기 떄문에 이 두개를 뽑아 낸다
2. 캡슐화 원칙 -> 캡슐화 대상으로 뽑아낸 오리의 행동을 어떻게 디자인 할지
    - 구현이 아닌 인터페이스에 맞춰서 프로그래밍 해야 한다
    - 이전 구현 방식, Duck 클래스에 구체적으로 구현하는 방식은 좋지 않다
3. 캡슐화 구현
    - 변수를 선언할 때는 보통 추상 클래스나 인터페이스 같은 상위 형식으로 선언해야 한다
      객체를 변수에 대입할 때 상위 형식을 구체적으로 구현한 형식이라면 어떤 객체든 집어넣을 수 있기 때문
        - 구현에 맞춘 코드 예시 (bad case)
            var d : :Dog = Dog();
            d.bark();
        - 인터페이스(상위 형식)에 맞춘 코드 에시 (good case)
            animal : Animal = new Dog()
            animal.makeSound();
        - 상위 형식의 인스턴스를 만드는 과정(new Dog()같은 식으로)을 직접 코드로 만드는 대신 구체적으로 구현된 객체를
          실행시에 대입하는 것이다 (best case)
            a = getAnimal()
            a.makeSound();
            - animal의 하위 형식 가운데 어떤 형식인지는 모른다. 단지 makeSound()에 대해 올바른 반응을 할 수 있으면 된다
 */

interface FlyBehavior {
    fun fly()
}

class FlyWithWings : FlyBehavior {
    override fun fly() {
        println("날고 있어요!")
    }
}

class FlyNoWay : FlyBehavior {
    override fun fly() {
        println("저는 못 날아요!")
    }
}

interface QuackBehavior {
    fun quack()
}

class Quack : QuackBehavior {
    override fun quack() {
        println("꽥")
    }
}

class MuteQuack : QuackBehavior {
    override fun quack() {
        println("~~조용~~")
    }
}

class Squeak : QuackBehavior {
    override fun quack() {
        println("삑")
    }
}



abstract class Duck(
    var quackBehavior: QuackBehavior,// 모든 Duck에는 QuackBehavior인터페이스를 구현하는 것에 대한 레퍼런스가 있다
    var flyBehavior: FlyBehavior
) {
    abstract fun display()

    fun performQuack() {
        quackBehavior.quack() // quack을 직접 처리 하는 대신 quackBehavior로 참조되는 객체에 그 행동을 위임한다
    }

    fun performFly() {
        flyBehavior.fly()
    }

    fun swim() {
        println("모든 오리는 물에 뜹니다. 가짜 오리도 뜨죠")
    }
}

class MallardDuck(
    quackBehavior: QuackBehavior = Quack(), // 캡슐화 구현 best case가 적용된 부분
    flyBehavior: FlyBehavior = FlyWithWings() // 캡슐화 구현 best case가 적용된 부분
) : Duck(quackBehavior, flyBehavior) {
    override fun display() {
        TODO("Not yet implemented")
    }
}

fun main() {
    val mallard = MallardDuck()
    mallard.performQuack()
    mallard.performFly()

    mallard.flyBehavior = FlyNoWay() //-> 동적으로 변경도 가능하다 (Strategy Pattern)
    mallard.performFly()
}










