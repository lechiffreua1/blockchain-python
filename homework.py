class Food:
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind

    def __repr__(self):
        return str(self.__dict__)

    def describe(self):
        print('Food name: {}, kind: {}'.format(self.name, self.kind))


food = Food('apple', 'fruit')
food.describe()


class FoodStatic:
    @staticmethod
    def describe(name, kind):
        print('Food name: {}, kind: {}'.format(name, kind))


FoodStatic.describe('apple', 'fruit')


class FoodClassMethod:
    name = 'default'
    kind = 'default'

    @classmethod
    def describe(cls):
        print('Food name: {}, kind: {}'.format(cls.name, cls.kind))


FoodClassMethod.name = 'apple'
FoodClassMethod.kind = 'fruit'
FoodClassMethod.describe()


class Meat(Food):
    def __init__(self, kind):
        name = 'meat'
        super().__init__(name, kind)

    def cook(self):
        print('I am cooking {} {}'.format(self.kind, self.name))


beef = Meat('beef')
beef.cook()


class Fruit(Food):
    def __init__(self, kind):
        name = 'fruit'
        super().__init__(name, kind)

    def clean(self):
        print('I amd cleaning {} {}'.format(self.kind, self.name))


apple = Fruit('apple')
apple.clean()


print(beef)
print(apple)
