from DI_example.domain.payment_factory import PaymentFactory
from DI_example.infra.payment_factory_impl import PaymentFactoryImpl
from DI_example.infra.payment_impl import TossPayment, NicePayment


def purchase_without_di():
    payment_type = 'toss'
    if payment_type == 'toss':
        TossPayment().pay()
    elif payment_type == 'nicepay':
        NicePayment().pay()


def purchase_with_di():
    payment_type = 'toss'
    payment_factory: PaymentFactory = PaymentFactoryImpl()
    payment = payment_factory.create_payment(payment_type)
    payment.pay()


purchase_with_di()
