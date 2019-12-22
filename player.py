import random
from battle import Battle
from enemy import Enemy


class Player:

    def __init__(self, name: str, hp: int, speed: int, power: int, character_class: str):
        self._name = name
        self._current_location_id = None
        self._class = character_class
        # exp and gold
        self._experience = 0
        self._lvl = 1
        self._gold = 0
        # basic stats
        self._power = power
        self._speed = speed
        self._health_points = hp
        self._health_points_max = self._health_points
        # items
        self._list_of_items = []

    def get_list_of_items(self):
        return self.get_list_of_items()

    def get_current_location(self):
        return self._current_location_id

    def move(self, new_location_id: int):
        self._current_location_id = new_location_id

    def get_name(self):
        return self._name

    def get_class(self):
        return self._class

    def get_exp(self):
        return self._experience

    def add_exp(self, new_exp: int):
        self._experience += new_exp

    def get_level(self):
        return self._lvl

    def level_up(self):
        exp_to_level_up = int(10*pow(1.2, self.get_level()))
        if self.get_exp() >= exp_to_level_up:
            self._lvl += 1
            self._experience -= exp_to_level_up

    def get_health_points(self):
        return self._health_points

    def get_health_points_max(self):
        return self._health_points_max

    def add_new_item(self, item: str):
        self.get_list_of_items().append(item)

    def remove_item(self, item: str):
        self.get_list_of_items().remove(item)

    def check_if_alive(self):
        return self.get_health_points() > 0


class Knight(Player):

    def __init__(self, name: str):
        super().__init__(name, 40, 5, 8, 'knight')
        # heavy armor of a knight reduces damage
        self.dmg_reduction = 2

    def normal_attack(self, battle: Battle, enemy):
        battle.round(enemy, self._power, self._speed, self.get_name())

    def heavy_attack(self, battle: Battle, enemy: Enemy):
        if random.randint(0, 101) <= 85:
            battle.round(enemy, int(self._power * 1.5), self._speed - 1, self.get_name())
        else:
            print('You have missed the enemy')
            battle.round([], 0, 100, self.get_name())

    def take_dmg(self, dmg: int):
        self._health_points -= (dmg - self.dmg_reduction)


class Wizard(Player):

    def __init__(self, name: str):
        super().__init__(name, 18, 7, 5, 'wizard')

        # basic stats
        self.magic_barrier = 4

    def aoe_attack(self, battle: Battle):
        battle.round(battle.list_of_enemies, int(self._power * 0.55), self._speed - 2)

    def magic_attack(self, battle: Battle, enemy: Enemy):
        if random.randint(0, 101) <= 90:
            battle.round(enemy, int(self._power * 1.2), self._speed)
        else:
            print('You have missed the enemy')
            battle.round([], 0, 100)

    def take_dmg(self, dmg: int):
        if self.magic_barrier > 0:
            self.magic_barrier -= dmg
            print('Your magic barrier has absorbed damage')
            if self.magic_barrier <= 0:
                print('Enemy broke your magic shield')
        else:
            self._health_points -= dmg


class Rouge(Player):

    def __init__(self, name: str):
        super().__init__(name, 20, 7, 11, 'rouge')

        # basic stats
        self._agility = 20

    def fast_attack(self, battle: Battle, enemy: Enemy):
        battle.round(enemy, self._power, self._speed + self._agility//10)

    def take_dmg(self, dmg: int):
        if random.randint(0, 101) > self._agility:
            self._health_points -= dmg
        else:
            print(f'You took {dmg} points of damage')


# Todo properties nigga
