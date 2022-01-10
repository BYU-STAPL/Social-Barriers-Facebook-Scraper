from abc import ABCMeta, abstractmethod

class IScrapeService(metaclass=ABCMeta):
    
    @abstractmethod
    def scrape(self, user_dto, browser):
        pass