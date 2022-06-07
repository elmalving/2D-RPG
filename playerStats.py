from Entity import Entity
from initPlayer import InitWindow
from Items import Item
import sqlite3
import random


class Player(Entity):
    def __init__(self):
        __player = InitWindow()
        __player.run()
        if not __player.username:
            exit()
        super().__init__(name=__player.username)
        self.money = 0
        db = sqlite3.connect('info.db')
        cursor = db.cursor()
        cursor.execute(f'SELECT money FROM {self.name}')
        db.commit()
        money = cursor.fetchone()
        if money:
            if money[0]:
                self.money = money[0]
        cursor.execute(f'SELECT weapon FROM {self.name}')
        db.commit()
        weapon = cursor.fetchone()
        if weapon:
            if weapon[0]:
                self.weapon = Item.from_id(weapon[0])
        cursor.execute(f'SELECT armor FROM {self.name}')
        db.commit()
        armor = cursor.fetchone()
        if armor:
            if armor[0]:
                self.armor = Item.from_id(armor[0])

    @property
    def health(self):
        return int(self._health + 3 * self.level ** 2 - 3)

    @health.setter
    def health(self, value):
        self._health = value

    def attack(self, target, stretch: float = 1):
        if stretch > 1:
            stretch = 1
        if target.armor:
            damage = random.randint(int(self.damage[0] * stretch) - target.armor.armor,
                                    int(self.damage[1] * stretch) - target.armor.armor)
        else:
            damage = random.randint(int(self.damage[0] * stretch), int(self.damage[1] * stretch))
        if target.health > damage:
            target.health -= damage
        else:
            damage = target.health
            target.health -= damage
        return damage
