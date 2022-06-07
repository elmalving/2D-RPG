class Entity:
    def __init__(self, name=None):
        self.name = name
        self._health = 40
        self._damage = (1, 2)
        self.level = 1
        self.weapon = None
        self.armor = None

    @property
    def damage(self):
        if self.weapon:
            return self.weapon.damage
        else:
            return self._damage
