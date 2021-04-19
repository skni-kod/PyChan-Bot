class BaseDatabaseClass:
    def load(self, data):
        for key in self.__dict__:
            if key not in data:
                return False
        self.__dict__ = data
        return self

    def json(self):
        return self.__dict__
