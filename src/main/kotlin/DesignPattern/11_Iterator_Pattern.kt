/*
이터레이터 패턴(Iterator Pattern)

### 정의 ###
- 컬렉션 구현 방법을 노출시키지 않으면서도 그 집합체 안에 들어있는 모든 항목에 접근할 수 있게 해주는 방법을 제공한다

### 목적 ###
- 바뀌는 부분을 캡슐화하라 -> 서로 다른 컬렉션 타입 때문에 반복 작업을 하는 방법이 다른 것을 일관화 시킨다
- 디자인 원칙 - 클래스를 바꾸는 이유는 한가지 뿐이어야 한다
    - 어떤 클래스에서 맡고 있는 모든 역할들은 나중에 코드 변화를 불어올 수 있다
      역할이 두 개 이상 있으면 바뀌술 있는 부분이 두 가지 이상이 되는 것이다
      따라서 원칙에 따라 한 클래스에서는 한 가지 역할만 맡도록 해야한다
- 응집도
    - 클래스는 또는 모듈이 특정 목적 또는 역할을 얼마나 일관되게 지원하는지를 나타내는 척도
      응집도가 높다는 것을 일련의 서로 연관된 기능이 묶여있다는 것을
      응집도가 낮다는 것은 서로 상관 없는 기능들이 묶여 있다는 것을 뜻한다

### 패턴에 사용된 기술 포인트 ###
- Iterator 라는 인터페이스에 의존한다
- 컬렉션 객체 안에 들어있는 모든 항목에 접근하는 방식이 통일되어 있으면 어떤 종류의 집합체에 대해서도 사용할 수 있는 다형적인 코드를 만들 수 있다
- 공통적인 인터페이스가 있으면 클라이언트 입장에서는 매우 편리해준다
    - 클라이언트와 객체 컬렉션의 구현이 분리 될 수 있기 때문
- 내부반복자, 외부 반복자
    - 아래 이터레이터 패턴구현은 외부반복자를 사용한다 (내부 반복자 사용도 가능)
      클라이언트에서 next()를 호출해서다음 항목을 가져오기 때문에 클라이언트가 반복작업을 제어한다
      -> 아이템을 꺼내와서 필요한 작업을 한다
    - 내부 반복자는 반복자 자신에 의해서 제어된다
      반복자가 다음 원소에 대해서 어떤 작업을 직접 처리하기 때문에 반복자한테 모든 원소에 대해서 어떤 일을 할 것인지 알려줘야 한다
      즉 클라이언트가 반복자한테 어떤 작업을 넘겨줘야 한다
      내부 반복자를 사용하는 경우 클라잉언트가 반복작업을 마음대로 제어할 수 없기 떄문에 외부반복자 보다 유연성이 떨어 진다
      하지만, 일을 넘겨주면 나머지는 알아서 하기 때문에 편한 경우도 있다
      -> 아이템에 해야할 일(함수)을 넘겨준다

### 문제 상황 ###
- A는 배열로 아이템을 관리하고, B는 리스트로 아이템을 관리하는데 A와B를 같이 관리할 필요가 생겼다

*/
// ### 해결책 ###
// - Iterator 패턴을 사용한다
interface Iterator {
    fun hasNext(): Boolean
    fun next(): Any
}

class MenuItem(val name: String, val description: String, val vegetarian: Boolean, val price: Double)


class DinnerInterator(
    val items: Array<MenuItem>
) : Iterator {
    var position: Int = 0

    override fun next(): Any {
        val menuItem: MenuItem = items[position]
        position += 1
        return menuItem
    }

    override fun hasNext(): Boolean {
        return if (position >= items.size || items[position] == null) false else true
    }
}

class DinnerMenu(
    val MAX_ITEMS: Int = 6,
    var numberOfItems: Int = 0,
) {
    val menuItems: Array<MenuItem>? = null

    init {
        addItem("채식주의자용 BLT", "맛있다", true, 1.22)
        addItem("베이컨", "맛있다", true, 1.22)
    }

    fun addItem(name: String, description: String, vegetarian: Boolean, price: Double) {
        val menuItem = MenuItem(name, description, vegetarian, price)
        if (numberOfItems >= MAX_ITEMS) println("메뉴가 꽉찼습니다")
        else {
            menuItems?.set(numberOfItems, menuItem)
            numberOfItems += 1
        }
    }

    // 적용된 DinnerInterator를 만들어주는 함수를 추가한다
    fun createIterator(): DinnerInterator {
        /*
          Iterator 인터페이스를 리턴한다
          클라이언트에서는 menuitems가 어떻게 관리되는지는 물론 DInnerMenuIterator가 어떤 식으로 구현되어 있는지 알필요가 없다
          그냥 반복자를 써서 메뉴에 들어 있는 항목들에 하나씩 접근 할 수만 있으면 된다
         */
        return DinnerInterator(menuItems!!)
    }
}

fun main() {
    fun printMenu(iterator: Iterator) {
        val menuItem: MenuItem = iterator.next() as MenuItem
        println(menuItem.name)
    }

    val dinnerInterator = DinnerMenu().createIterator()

    printMenu(dinnerInterator)
}