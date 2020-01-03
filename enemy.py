class Enemy:
    """
    This class represents basic template of an enemy
    """
    def __init__(self, name: str, power: int, speed: int, hp: int, exp: int, gold: int):
        """
        Initializes enemy object
        :param name: enemy's name
        :param power: power of enemy's attacks
        :param speed: speed of enemy's attacks
        :param hp: enemy's health points
        :param exp: reward in exp for killing enemy
        :param gold: reward in gold for killing enemy
        """
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
        """
        Reduces enemy's health
        :param dmg: damage that enemy is hit with
        """
        self._hp -= dmg

    def check_if_alive(self):
        """
        :return: Checks if Enemy is alive
        """
        return self.hp > 0

    @property
    def rewards(self):
        return self._exp_reward, self._gold_reward


enemies = {'thief': Enemy('thief', 4, 5, 15, 15, 10)}
