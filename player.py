import random
from battle import Battle
from enemy import Enemy
from gamedisplay import Display


class Player:

    def __init__(self, name: str, hp: int, speed: int, power: int, character_class: str, display: Display):
        # basic info
        self._name = name
        self._current_location_id = None
        self._class = character_class
        self._battle = None
        self._display = display
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

    # basic info methods

    @property
    def name(self):
        return self._name

    @property
    def current_location(self):
        return self._current_location_id

    @current_location.setter
    def current_location(self, new_location_id: int):
        self._current_location_id = new_location_id

    @property
    def character_class(self):
        return self._class

    @property
    def battle(self):
        return self._battle

    @battle.setter
    def battle(self, new_battle: Battle):
        self._battle = new_battle
        if self.battle:
            self.battle.display.start_a_battle()

    @property
    def display(self):
        return self._display

    # exp, lvl, gold methods

    @property
    def exp(self):
        return self._experience

    def add_exp(self, new_exp: int):
        self._experience += new_exp
        self.display.add_info(f'You have got new {new_exp} experience!')
        return self.level_up()

    @property
    def level(self):
        return self._lvl

    def level_up(self):
        exp_to_level_up = int(10*pow(1.2, self.level))
        if self.exp >= exp_to_level_up:
            self._lvl += 1
            self._experience -= exp_to_level_up
            self.display.add_info(f'You have leveled up! You are currently on level {self.level}')
        return self.exp >= exp_to_level_up

    @property
    def gold(self):
        return self._gold

    def add_gold(self, gold):
        self._gold += gold
        self.display.add_info(f'You have earned {gold} gold!')

    def remove_gold(self, gold):
        if self._gold - gold >= 0:
            self._gold -= gold
        return self._gold - gold >= 0

    # basic stats methods

    @property
    def power(self):
        return self._power

    def power_increase(self, value):
        self._power += value

    @property
    def speed(self):
        return self._speed

    def speed_increase(self, value):
        self._speed += value

    @property
    def health_points(self):
        return self._health_points

    @property
    def health_points_max(self):
        return self._health_points_max

    def heal(self, healed_hp_points):
        self._health_points = min(self.health_points + healed_hp_points, self.health_points_max)

    def check_if_alive(self):
        return self.health_points > 0

    # items methods

    def get_list_of_items(self):
        return self.get_list_of_items()

    def add_new_item(self, item: str):
        self.get_list_of_items().append(item)

    def remove_item(self, item: str):
        self.get_list_of_items().remove(item)


class Knight(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 40, 5, 8, 'knight', display)
        # heavy armor of a knight reduces damage
        self.dmg_reduction = 2

    def normal_attack(self, enemy):
        self.battle.round(enemy, self.power, self.speed, self.name)

    def heavy_attack(self, enemy: Enemy):
        if random.randint(0, 101) <= 85:
            self.battle.round(enemy, int(self.power * 1.5), self.speed - 1, self._name)
        else:
            self.battle.get_display().add_info('You have missed the enemy')
            self.battle.round([], 0, 100, self.name)

    def take_dmg(self, dmg: int):
        self._health_points -= (dmg - self.dmg_reduction)


class Wizard(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 18, 7, 5, 'wizard', display)
        self._magic_barrier = 4

    @property
    def magic_barrier(self):
        return self._magic_barrier

    def aoe_attack(self):
        self.battle.round(self.battle.list_of_enemies, int(self.power * 0.55), self.speed - 2)

    def magic_attack(self, enemy: Enemy):
        if random.randint(0, 101) <= 90:
            self.battle.round(enemy, int(self.power * 1.2), self.speed)
        else:
            self.battle.get_display().add_info('You have missed the enemy')
            self.battle.round([], 0, 100)

    def take_dmg(self, dmg: int):
        if self.magic_barrier > 0:
            self._magic_barrier -= dmg
            self.battle.get_display().add_info('Your magic barrier has absorbed damage')
            if self.magic_barrier <= 0:
                self.battle.get_display().add_info('Enemy broke your magic shield')
        else:
            self._health_points -= dmg


class Rouge(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 20, 7, 11, 'rouge', display)
        self._agility = 20

    @property
    def agility(self):
        return self._agility

    def agility_increase(self, value):
        self._agility += value

    def life_stealing_blade_attack(self, enemy: Enemy):
        self.battle.round(enemy, self.power//2, self.speed + self.agility // 10)
        self.heal(self.power//4)

    def fast_attack(self, enemy: Enemy):
        self.battle.round(enemy, self.power, self.speed + self.agility//10)

    def take_dmg(self, dmg: int):
        if random.randint(0, 101) > self.agility:
            self._health_points -= dmg
        else:
            self.battle.get_display().add_info(f'You took {dmg} points of damage')
