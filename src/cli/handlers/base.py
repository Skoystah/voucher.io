import config

class BaseHandler():
    def __init__(self, config: config.Config) -> None:
        self._config = config

    def handle(self, *args):
        pass
