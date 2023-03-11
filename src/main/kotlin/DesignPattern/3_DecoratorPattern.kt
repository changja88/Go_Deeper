/*
데코레이터 패턴(Decorator Pattern)
### 정의 ###
- 객체에 추가적인 요건을 동적으로 첨가한다. 데코레이터는 서브클래스를 만드는 것을 통해서 기능을 유연하게 확장할 수 있는 방법을 제공한다

- 데코레이터의 슈퍼클러스는 자신이 장식하고 있는 객체의 슈퍼클래스와 같다 (결국, 모든 클래스에서 beverage가 슈퍼클래스이다)
- 한 객체를 여러 개의 데코레이터로 감쌀 수 있다
- 데코레이터는 자신이 감싸고 있는 객체와 같은 슈퍼클래스를 가지고 있기 때문에 원래 객체가 들어갈 자리에 데코레이터 객체를 넣어도 상관이 없다
- 객체는 언제든지 감쌀 수 있기 때문에 실행 중에 필요한 데코레이터를 마음데로 적용할 수 있다
- 데코레이터 객체를 래퍼(Wrapper)라고 생각하면 된다
    - 일반커피 < 모카 < 휘핑
    - cost를 계산 할 때는 휘핑의 cost()를 사용하면 된다

### 목적 ###
디자인 원칙 : (Open-closed Principle, OCP)클래스는 확장에 대해서는 열려 있어야 하지만 코드 변경에 대해서는 닫혀 있어야 한다
- 결국 데코레이터 패턴은 클래스를 건들지 않고 확장하기 위한 방법이다

### 패턴에 사용된 기술 포인트 ###
- 데코레이터 패턴의 단점을 알고 사용하는게 중요하다
단점
1>
- 자잘한 클래스들이 많이 만들어지는 경우가 많다
2>
- 구상 구성요소의 형식을 알아내서 그 결과를 바탕으로 어떤 작업을 처리하는 코드에 데코레이터 패턴을 적용하면 망한다
- 추가 구성요소 형식을 바탕으로 돌아가는 코드에 대해서 데코레이터 패턴을 적용해야 한다
3>
- 데코레이터를 빼먹는 실수를 할 수가 있다 (휘핑을 빼먹는 다던지..)
- 보통 데코레이터 패턴은 일반적으로 팩토리나 빌더 같은 다른 패턴을 써서 만들고 사용하게 된다
4>
- 감싸져 있는 객체에 특정 작업을 하는 것은 적합하지 않다
- 데코레이터는 그 데코레이터가 감싸고 있는 객체에 행동을 추가하기 위한 용도로 만들어 졌다, 여러 단계의 데코레이터를
  파고들어가서 어떤 작업을 해야 한다면, 원래 데코레이터 패턴이 만들어진 의도와 어긋난다

### 문제 상황 ###
- 스타벅스에서 커피를 구성할 때, Beverage 클래스를 최상위 클래스로 두고, 이를 상속 받는 클래스들이 존재 한다
  (에스프레소, 디카페인 커피, 모카 커피 등등)
- 문제는 서브 클래스들이 많아도 너무 많다 (음료의 종류가 엄청 많기 때문, 각각의 커피 별로 두유 여부, 휘핑 여부 등등 옵션도 존재)

### 해결책 ###
- 휘핑, 두유 등등의 추가 옵션 여부는 슈퍼 클래스에 만든다 -> 서브 클래스의 갯수를 획기적으로 줄일 수 있다
- 문제점
    - 옵션(첨가물)의 종류가 많아지면 새로운 메소드를 추가해야 하고, 슈퍼클래스의 cost()메소드도 고쳐야한다
    - 특정 옵션이 들어가면 안되는 새로운 음료가 나올경우 문제가 발생한다
*/
abstract class Beverage(var description: String = "제목 없음") {

    abstract fun cost(): Double
}

abstract class CondimentDecorator : Beverage() {
// 첨가물 데코레이터
}

class Espresso(description: String = "에스프레소") : Beverage() {
    override fun cost(): Double = 1.99
}

class HouseBlend(description: String = "하우스 블렌드 커피") : Beverage() {
    override fun cost(): Double = 0.89

}

class Mocha(val beverage: Beverage) : CondimentDecorator() {

    init {
        description = beverage.description + " 모카"
    }

    override fun cost(): Double = 0.2 + beverage.cost()
}


fun main() {
    val beverage: Beverage = Espresso()
    println(beverage.description)

    var beverage2: Beverage = HouseBlend()
    beverage2 = Mocha(beverage2)
    println(beverage2.description)
    println(beverage2.cost())

}
