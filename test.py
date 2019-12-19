class Test:
    def __init__(self):
        self.a = 1

    def __repr__(self):
        return str(self.__dict__)


test1 = Test()

print(str(test1))

