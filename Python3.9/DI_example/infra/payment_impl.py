from DI_example.domain.payment import Payment


class NicePayment(Payment):
    def pay(self):
        print('nice pay')


class TossPayment(Payment):
    def pay(self):
        print('toss pay')


