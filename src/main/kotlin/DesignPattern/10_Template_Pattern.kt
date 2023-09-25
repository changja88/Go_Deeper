/*
템플릿 패턴(Template Pattern)
### 정의 ###
- 메소드에서 알고리즘의 골격을 정의한다. 알고리즘의 여러 단계 중 일부는 서브클래스에서 구현할 수 있다. 템플릿 메소드를 이용하면 알고리즘의 구조는 그대로
  유지하면서 서브클래스에서 특정 단계를 재정의할 수 있습니다

### 목적 ###
- 템플릿 메소드를 제공해서 서브클래스가 구현할 수 있도록 하게 해준다
- 헐리우드 원칙 : 먼저 연락하지 마세요, 저희가 연락 드리겠습니다
    - 의존성 부패(dependency rot)를 방지 할 수 있다
    - 어떤 고수준 구성요소가 저수준 구성요소에 의존하고, 그 저수준 구성요소는 다시 고수준 구성요소에 의존하고, 그 고수준 요소는 다른 것에 의존하고...
    - CaffeinBeverage(고수준) Coffee, Tea(저수준)
        - Coffee, Tea (저수준)는 호출 당하기 전까지는 절대로 추상 클래스를 직접 호출 하지 않는다
    - "의존성 뒤집기"와의 관계
        - 객체를 분리시킨다는 하나의 목표를 공유하고 있긴하지만, 디자인상의 의존성을 피하는 방법에 있어서 의존성 뒤집기 원칙이 훨씬 더 강하고 일반적인 내용을 담고 있다
        - 의존성 뒤집기는 될 수 있으면 구상 클래스 사용을 줄이고 대신 추상화된 것을 사용해야 한다는 원칙이다
          할리우드 원칙은 저수준 구성요소들을 다양하게 사용할 수 있으면서도, 다른 클래스가 그러한 구성요소에 너무 의존하지 않게 만들어주는 디자인 기법이다

- 다른 패턴과의 관계
    - 템플릿 메소드 패턴 -> 알고리즘의 일부 단계를 구현하는 것을 서브클래스에서 처리한다
    - 스트래티지 패턴 -> 바꿔쓸수 있는 행동을 캡슐화하고, 어떤 행동을 사용할지는 서브클래스에 맡긴다
    - 팩토리 메소드 패턴 -> 어떤 구상 클래스를 생성할지를 서브클래스에서 결정한다

### 패턴에 사용된 기술 포인트 ###
- 후크(hook)
    - 추상 클래스에서 선언되는 메소드긴하지만 기본적인 내용만 구현되어 있거나 아무 코드도 들어있지 않은 메소드이다
      이렇게 하면 서브클래스 입장에서는 다양한 위치에서 알고리즘에 끼어들 수 있다
    - 후크는 다양하게 활용될 수 있다


### 문제 상황 ###
- Coffee와 Tea는 사실 거의 비슷해 보인다 어떻게 추상화를 시켜야 할까?
*/
class Coffee() {
    fun prepareRecipe() {
        boilWater(); brewCoffeeGrinds(); pourInCup(); addSugarAndMilk()
    }

    fun boilWater() {}
    fun brewCoffeeGrinds() {}
    fun pourInCup() {}
    fun addSugarAndMilk() {}
}

class Tea() {
    fun prepareRecipe() {
        boilWater(); steepTeaBag(); purInCup(); addLemon()
    }

    fun boilWater() {}
    fun steepTeaBag() {}
    fun addLemon() {}
    fun purInCup() {}
}

// ### 해결책 ###
// - 템플릿 메소드 도입
abstract class CaffeinBeverage() {
    final fun prepareRecipe() {
        // brew와 addCondiments로 좀더 일반화된 메소드를 만들어서 추상화 시켰다
        // 서브클래스에서 알고리즘의 각 단계를 마음대로 건드리느 ㄴ것을 방지하기 위해서 final로 선언합니다
        boilWater(); brew(); pourInCup(); addCondiments()
    }

    abstract fun brew() // 서브클래스에서 처리되는 메소드
    abstract fun addCondiments() // 서브클래스에서 처리되는 메소드
    fun boilWater() {}
    fun pourInCup() {}
    fun hook() {
        // 기본적으로 아무것도 하지 않는 구상 메소드를 정의할 수도 있다
        // 이런 메소드는 후크(hook)라고 부른다. 서브 클래스에서 오버라이드할 수 있지만, 반드시 그래야 하는 것은 아니다
    }
}

class Tea2() : CaffeinBeverage() {
    override fun brew() {}
    override fun addCondiments() {}
}

class Coffee2() : CaffeinBeverage() {
    override fun brew() {}
    override fun addCondiments() {}
}

/*
후크(hook)메소드
- 템플릿 메소드가 정의 되어있는 추상 클래스에 존재하지만, 기본적인 내용만 구현되어 있거나 아무 코드도 들어있지 않은 메소드이다
- 때문에, 서브클래스 입장에서는 다양한 위치에서 알고리즘에 끼어들 수 있고, 무시 할 수도 있다

언제 후크 메소드를 써야하고, 추상 메소드를 써야 하는가?
- 알고리즘의 특정 단계를 제공해야만 하는 경우에는 추상 메소드를 써야 한다
- 알고리즘의 특정 부분이 선택적으로 적용된다든가 하는 경우에는 후크를 사용하면 된다 (서브클래스에서 반드시 구현 해야하는 것은 아니기 때문)
- 템플릿 메소드 앞으로 일어날 일 또는 막 일어난 일에 대해 서브클래스에서 반응할 기회를 제공하기 위한 용도로도 사ㅛㅇ가능
 */
abstract class CaffeinBeverageWithHook {
    fun prepareRecipe() {
        boilWater()
        brew()
        pourInCup()
        if (customerWantsCondiments()) {
            addCondiments()
        }
    }

    abstract fun brew()
    abstract fun addCondiments()

    fun pourInCup() {
        println("컵에 따르는중")
    }

    fun boilWater() {
        println("물을 끓이는 중")
    }

    open fun customerWantsCondiments(): Boolean {
        // 후크 메소드이다
        // - 별 구현이 없는 기본 메소드를 구현해 놓는다 (true만 리턴할 뿐 아무런 일도 하지 않는다)
        // - 서브 클래스에서 필요에 따라 오버라이드 할 수 있는 메소드이므로 후크 메소드이다
        return true
    }
}

// 후크메소드 활용 예시
class CoffeeWithHook : CaffeinBeverageWithHook() {
    override fun brew() {
    }

    override fun addCondiments() {
    }

    override fun customerWantsCondiments(): Boolean {
        val answer: String = getUserInput()
        if (answer.startsWith("Y")) return true
        else return false
    }

    fun getUserInput(): String {
        return "Y"
    }
}

