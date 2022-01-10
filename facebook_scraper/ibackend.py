from abc import ABCMeta, abstractmethod

class IBackend(metaclass=ABCMeta):
    
    @abstractmethod
    def store_data(self, user_dto):
        pass