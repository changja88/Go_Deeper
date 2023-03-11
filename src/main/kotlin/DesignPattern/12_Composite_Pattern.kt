/*
컴포지트 패턴(Composite Pattern)

### 정의 ###
- 객체들을 트리 구조로 구성하여 부분과 전체를 나타내는 계층구조로 만들수 있다.
  이 패턴을 이용하면 클라이언트에서 개별 객체와 다른 객체들로 구성된 복합객체를 똑같은 방법으로 다룰 수 있다
- Composite : 합성물

### 목적 ###
- 복합 객체와 개별 객체에 대해 똑같은 작업을 적용할 수 있다.
  즉, 복합객체와 개별 객체를 구분할 필요가 없어진다

### 패턴에 사용된 기술 포인트 ###
- 부분-전체 계층 구조를 생성한다, 부분들들이 모여있지만, 모든 것을 하나로 묶어서 전체로 다룰수 있는 구조
    - 부분들이 모여있지만 전체로 다룬다 -> Composite와 leaf를 하나로 다룬다
    - composite 와 leaf 모두 component 타입 이기 때문에 하나로 다룰 수 있다
    - component는 compsite와 leaf모두 상속 받기 때문에 compsite, leaf가 필요한 모든 행동에 대한 정의가 있어야 한다

- 아래와 같은 구조를 만든다
  Client(Waitress) -> Component(MenuComponent) <- Composite(Menu, 복합객체)
                                               <- Leaf(MenuItem, 개별객체)
    - Component : 복합 객체내에 들어 있는 모든 객체들에 대한 인터페이스를 정의하고, leaf에 대한 메소드까지 정의 한다
    - Composite : 자식이 있는 구성 요소의 행동을 정의하고 자식 구성요소를 저장하는 역할을 한다
                  Leaf와 과련된 기능도 구현해야 한다.
    - Leaf : 자식이 없다
             원소에 대한 행동을 정의한다 (Composite에서 지원하는 기능을 구현하면 된다)



- 다른 패턴과의 차이점
    - 스테이트 패턴 : 어떤 상태가 바뀜에 따라 객체의 행동을 바꿀 수 있습니다
    - 어답터 패턴 : 하나 이상의 클래스의 인터페이스를 변환합니다
    - 이터레이터 패턴 : 컬렉션의 구현을 드러내지 않으면서도 컬렉션에 있는 모든 객체들에 대해 반복작업을 할 수 있습니다
    - 퍼사드 패턴 : 일련의 클래스들에 대한 인터페이스를 단순화시킵니다
    - 컴포지트 패턴 : 클라이언트에서 객체 컬렉션과 개별 객체를 똑같은 식으로 처리할 수 있습니다
    - 옵저버 패턴 : 어떤 상태가 변경되었을 때 일련의 객체들한테 연락을 할 수 있습니다


### 문제 상황 ###
- 전체 메뉴 -> 팬케이크 하우스 메뉴
          -> 객체마을 식당 메뉴  -> 디저트 메뉴 -> 메뉴 아이템
  위와 같이 트리구조를 처리해야한다

### 해결책 ####
- 컴포지트 패턴을 도입한다
    - 메뉴 아이템도 다른 객체가 들어 있지 않을 뿐 결국 메뉴이다
*/

abstract class MenuComponent {
    open fun add(menuComponent: MenuComponent) {
        throw UnsupportedOperationException()
    }

    open fun remove(menuComponent: MenuComponent) {
        throw UnsupportedOperationException()
    }

    open val name: String
        get() {
            throw UnsupportedOperationException()
        }
    open val description: String
        get() {
            throw UnsupportedOperationException()
        }

    open fun print() {
        throw UnsupportedOperationException()
    }
}


class Menu(
    override val name: String, override val description: String
) : MenuComponent() {
    val menuComponents = ArrayList<MenuComponent>()

    override fun add(menuComponent: MenuComponent) {
        menuComponents!!.add(menuComponent)
    }

    override fun remove(menuComponent: MenuComponent) {
        menuComponents!!.remove(menuComponent)
    }

    override fun print() {
        val iterator = menuComponents.iterator()
        while (iterator.hasNext()) {
            val menuComponent = iterator.next()
            menuComponent.print()
        }
    }
}


class MenuItem1(
    override var name: String, override val description: String, val vegetarian: Boolean, val price: Double
) : MenuComponent() {

    override fun print() {
        println("" + name + description + price)
    }
}


class Waitress(val allMenues: MenuComponent) {
    fun printMenu() {
        allMenues.print()
    }
}

fun main() {
    val pancakeHouseMenue: MenuComponent = Menu("팬케이크 하우스 메뉴", "아침메뉴")
    val dinnerMenu: MenuComponent = Menu("객체마을 식당메뉴", "점심메뉴")
    val cafeMenu: MenuComponent = Menu("카페 메뉴", "저녁메뉴")
    val desseertMenu: MenuComponent = Menu("디저트메뉴", "디저트메뉴")

    val allMenu: MenuComponent = Menu("전체메뉴", "전체메뉴")
    allMenu.add(pancakeHouseMenue)
    allMenu.add(dinnerMenu)
    allMenu.add(cafeMenu)

    dinnerMenu.add(MenuItem1("파스타", "파스타", true, 3.89))
    dinnerMenu.add(desseertMenu)
    desseertMenu.add(MenuItem1("애플 파이", "바삭", false, 1.2))

    val waitress = Waitress(allMenu)
    waitress.printMenu()

}










