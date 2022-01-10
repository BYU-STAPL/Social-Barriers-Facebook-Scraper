from abc import ABCMeta, abstractmethod

class ISheet(metaclass=ABCMeta):
    
    @abstractmethod
    def store_data(self, user_dto):
        pass