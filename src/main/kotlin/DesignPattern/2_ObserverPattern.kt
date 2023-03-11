/*
옵저버 패턴(Observer Pattern)
### 정의 ###
- 한 객체의 상태가 바뀌면 그 객체에 의존하는 다른 객체들에게 연락이 가고 자동으로 내용이 갱신되는 방식으로 일대다 의존성을 정의한다
- 출판사(subject) + 구독자(observer) = 옵저버 패턴

### 목적 ###
- 디자인 원칙 : 서로 상호작용을 하는 객체 사이에서는 가능하면 느슨한 결합을 하는 디자인을 사용해야 한다

### 패턴을 사용된 기술 포인트 ###
- 느슨한 결합(Loose coupling) : 두 객체가 상호작용을 하긴 하지만 서로에 대해 잘 모르는 것을 의미
- 느슨하게 결합하는 디자인을 사용하면 변경 사항이 생겨도 무난히 처리할 수 있는 유연한 객체지향 시스템을 구축 할 수 있다
  객체 사이의 상호의존성을 최소화할 수 있기 때문
- 옵저버 패턴이 구체적으로 어떻게 느슨한 결합인가
    - 출판사가 구독자에 대해서 아는 것은 구독자가 특정 인터페이스를 구현한다는 것 뿐이다
    - 옵저버는 언제든지 새로 추가할 수 있다
    - 새로운 형식의 옵저버를 추가하려고 할 때도 출판사를 전형 변경할 필요가 없다
    - 출판사와 옵저버는 서로 독립적으로 재상용할 수 있다
    - 출판사나 옵저버가 바뀌더라도 서로한테 전형 영향을 주지 않는다 (느슨한 결합의 장점)

### 문제 상황 ###
WeatherData 객체를 사용하여 현재 조건, 기상 통계, 기상 예측, 이렇게 세 항목을 디스플레이 장비에서 갱신해가면서 보여줘야 한다
    - WeatherData클래스에는 세가지 측정값을 알아내기 위한 게터 메소드가 있다
    - 새로운 기상 측정 데이터가 나올 때마다 measurementsChanges()메소드가 호출된다 -> 어떤 원리로 동작하는지는 알 필요가 없다
    - 기상 데이터를 사용하는 세 개의 디스플레이 항목을 구현해야 하며, 새로운 측정값이 들어올 때마다 디스플레이를 갱신해야 한다
    - 시스템이 확장 가능해야한다. 다른 개발자들이 별도의 디스플레이 항목을 만들수 있도록 해야하고, 사용자들이 애플리케이션에서 마음대로
      디스플레이 항목을 추가/제거 할 수 있도록 해야 한다
 */

interface Subject {
    fun registerObserver(o: Observer)
    fun removeObserver(o: Observer)
    fun notifyObservers()
}

interface Observer {
    fun update(temp: Float, humidity: Float, pressure: Float)
}

interface DisplayElement {
    fun display()
}

class WeatherData(
    var observers: ArrayList<Observer> = ArrayList()
) : Subject {
    var temperature: Float = 0f
    var humidity: Float = 0f
    var pressure: Float = 0f


    override fun notifyObservers() {
        for (i in 0..observers.size - 1) {
            val observer = observers.get(i)
            observer.update(temp = temperature, humidity = humidity, pressure = pressure)
        }
    }

    fun measurementsChanged() {
        notifyObservers()
    }

    fun setMeasurements(temperature: Float, humidity: Float, pressure: Float) {
        this.temperature = temperature
        this.humidity = humidity
        this.pressure = pressure
        measurementsChanged()
    }

    override fun removeObserver(o: Observer) {
        val i: Int = observers.indexOf(o)
        if (i > 0) observers.removeAt(i)
    }

    override fun registerObserver(o: Observer) {
        observers.add(o)
    }
}

class CurrentConditionsDisplay(val weatherData: Subject) : Observer, DisplayElement {
    var temperature: Float = 0f
    var humidity: Float = 0f
    var pressure: Float = 0f

    init {
        weatherData.registerObserver(this)
    }


    override fun update(temp: Float, humidity: Float, pressure: Float) {
        this.temperature = temperature
        this.humidity = humidity
        display()
    }

    override fun display() {
        println("Current conditions : " + temperature + humidity + pressure)
    }
}

fun main() {
    val weatherData = WeatherData()
    val currentDisplay = CurrentConditionsDisplay(weatherData)
    weatherData.setMeasurements(80f, 65f, 30.4f);
}

