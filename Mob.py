from itertools import count
from Entity import Entity
from random import randint
from Items import Item


class Mob(Entity):
    __ids = count(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = next(self.__ids)

        last_id = ''
        for i in str(Item.id()):
            if i.isdigit():
                last_id += f'{i}'

        drop = []
        for j in range(int(last_id)):
            if Item.from_id(j).level == self.level:
                drop.append(Item.from_id(j))

        self.drop = drop

    def die(self):
        for i in self.drop:
            if i.dropRate >= randint(1, 100):
                yield i

    @property
    def health(self):
        return int(self._health + 2 * self.level ** 2 - 2)

    @health.setter
    def health(self, value):
        self._health = value

    def say(self):
        print("You're still hoping for win? HAHA")


class Zombie(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'Zombie'
        self.level = 1
