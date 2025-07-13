from abc import abstractmethod
from config import Config

class BaseHandler():
    @abstractmethod
    def handle(self, config: Config, *args):
        pass

