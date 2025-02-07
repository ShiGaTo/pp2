class Printer:
    string = ""

    def getString(self):
        self.string = input()

    def printString(self):
        print(self.string.upper())


class Shape:
    area = 0

    def printArea(self):
        print(self.area)


class Sqare(Shape):
    length = 0

    def __init__(self, length):
        super().__init__()
        self.length = length
        self.area = length * length


class Rectangle(Shape):
    length = 0
    width = 0

    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width
        self.area = length * width


class Point:
    x, y = 0, 0

    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def show(self):
        print(f"x: {self.x}, y: {self.y}")

    def move(self, new_x, new_y):
        self.x, self.y = new_x, new_y

    def dist(self, point2):
        return (abs(self.x - point2.x) ** 2 + abs(self.y - point2.y) ** 2) ** .5


class Account:
    owner = None
    balance = 0

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, value):
        self.balance += value

    def withdraw(self, value):
        if self.balance < value:
            raise "Cannot exceed the available balance"
        self.balance -= value


# Lambda:
nums = [i for i in range(-10, 100)]

print(list(filter(
    lambda num: False if num < 2 else all([num % i != 0 for i in range(2, int(num ** .5 + 1))]),
    nums
)))