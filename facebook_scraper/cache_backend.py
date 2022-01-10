from .ibackend import IBackend

class CacheBackend(IBackend):
    def __init__(self):
        self.user_data = {} 
    def store_data(self, user_dto):
        self.user_data = user_dto.user_data