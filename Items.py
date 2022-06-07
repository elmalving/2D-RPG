import weakref
from itertools import count
from math import ceil, floor


class Item:
    id_to_item = weakref.WeakValueDictionary()
    __ids = count(0)

    def __init__(self, name, level, rarity, type, image=None):
        self.id = next(self.__ids)
        self.id_to_item[self.id] = self
        self.name = name
        self.level = level
        self.rarityName = rarity.rarity
        self.rarityColor = rarity.color
        self.type = type
        self.image = image
        self.dropRate = rarity.dropRate
        self.price = ceil(self.level * 100 / self.dropRate + self.level ** 2 / self.dropRate)

    @classmethod
    def from_id(cls, id):
        return cls.id_to_item[id]

    @classmethod
    def id(cls):
        return cls.__ids


class Rarity:
    def __init__(self, name, color, dropRate):
        self.rarity = name
        self.color = color
        self.__dropRate = dropRate

    @property
    def dropRate(self):
        return self.__dropRate


class Weapon(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def from_id(self):
        raise TypeError("Method from_id is not supported in class Weapon")

    @property
    def damage(self):
        if self.type == 'close':
            base = self.level * 1.88
            return ceil(base), ceil(base + self.level / 2.6)
        if self.type == 'long-range':
            base = self.level * 3.33
            return ceil(base), ceil(base + self.level / 2.6)


class Armor(Item):
    def __init__(self, **kwargs):
        super().__init__(type='armor', **kwargs)

    def from_id(self):
        raise TypeError("Method from_id is not supported in class Armor")

    @property
    def armor(self):
        base = self.level * 1.33
        return floor(base), ceil(base + self.level / 2)
