from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def work(self):
        pass


class ServiceImpl(Service):

    def work(self):
        print('구체 클래스가 일한다')


class ServiceFactory(ABC):
    @abstractmethod
    def makeSvc(self):
        pass


class ServiceFactoryImpl(ServiceFactory):

    def makeSvc(self):
        return ServiceImpl()
