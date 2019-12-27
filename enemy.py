class Enemy:
    def __init__(self, name: str, power: int, speed: int, hp: int, exp: int, gold: int):
        self._name = name
        self._power = power
        self._speed = speed
        self._hp = hp
        self._hp_max = hp
        self._exp_reward = exp
        self._gold_reward = gold

    @property
    def name(self):
        return self._name

    @property
    def power(self):
        return self._power

    @property
    def speed(self):
        return self._speed

    @property
    def hp(self):
        return self._hp

    @property
    def hp_max(self):
        return self._hp_max

    def take_dmg(self, dmg):
        self._hp -= dmg

    def check_if_alive(self):
        return self.hp > 0

    @property
    def rewards(self):
        return self._exp_reward, self._gold_reward


enemies = {'thief': Enemy('thief', 4, 5, 15, 15, 10)}
