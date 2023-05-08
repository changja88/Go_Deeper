from DI_example.domain.payment_factory import PaymentFactory
from DI_example.infra.payment_impl import NicePayment, TossPayment


class PaymentFactoryImpl(PaymentFactory):

    def create_payment(self, type: str):
        if type == 'nicepay':
            return NicePayment()
        if type == 'toss':
            return TossPayment()
