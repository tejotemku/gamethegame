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

    def get_name(self):
        return self._name

    def get_current_location(self):
        return self._current_location_id

    def move(self, new_location_id: int):
        self._current_location_id = new_location_id

    def get_class(self):
        return self._class

    def get_battle(self):
        return self._battle

    def set_battle(self, battle: Battle):
        self._battle = battle
        if self.get_battle():
            self.get_battle().display.start_a_battle()

    def get_display(self):
        return self._display

    # exp, lvl, gold methods

    def get_exp(self):
        return self._experience

    def get_level(self):
        return self._lvl

    def add_exp(self, new_exp: int):
        self._experience += new_exp
        self.get_display().add_info(f'You have got new {new_exp} experience!')
        return self.level_up()

    def level_up(self):
        exp_to_level_up = int(10*pow(1.2, self.get_level()))
        if self.get_exp() >= exp_to_level_up:
            self._lvl += 1
            self._experience -= exp_to_level_up
            self.get_display().add_info(f'You have leveled up! You are currently on level {self.get_level()}')
        return self.get_exp() >= exp_to_level_up

    def get_gold(self):
        return self._gold

    def add_gold(self, gold):
        self._gold += gold
        self.get_display().add_info(f'You have earned {gold} gold!')

    def remove_gold(self, gold):
        if self._gold - gold >= 0:
            self._gold -= gold
        return self._gold - gold >= 0

    # basic stats methods

    def get_power(self):
        return self._power

    def get_speed(self):
        return self._speed

    def get_health_points(self):
        return self._health_points

    def get_health_points_max(self):
        return self._health_points_max

    def heal(self, healed_hp_points):
        self._health_points = min(self.get_health_points() + healed_hp_points, self.get_health_points_max())

    def check_if_alive(self):
        return self.get_health_points() > 0

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
        self.get_battle().round(enemy, self.get_power(), self.get_speed(), self.get_name())

    def heavy_attack(self, enemy: Enemy):
        if random.randint(0, 101) <= 85:
            self.get_battle().round(enemy, int(self.get_power() * 1.5), self.get_speed() - 1, self._name)
        else:
            self.get_battle().get_display().add_info('You have missed the enemy')
            self.get_battle().round([], 0, 100, self.get_name())

    def take_dmg(self, dmg: int):
        self._health_points -= (dmg - self.dmg_reduction)


class Wizard(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 18, 7, 5, 'wizard', display)
        self._magic_barrier = 4

    def get_magic_barrier(self):
        return self._magic_barrier

    def aoe_attack(self):
        self.get_battle().round(self.get_battle().list_of_enemies, int(self.get_power() * 0.55), self.get_speed() - 2)

    def magic_attack(self, enemy: Enemy):
        if random.randint(0, 101) <= 90:
            self.get_battle().round(enemy, int(self.get_power() * 1.2), self.get_speed())
        else:
            self.get_battle().get_display().add_info('You have missed the enemy')
            self.get_battle().round([], 0, 100)

    def take_dmg(self, dmg: int):
        if self.get_magic_barrier() > 0:
            self._magic_barrier -= dmg
            self.get_battle().get_display().add_info('Your magic barrier has absorbed damage')
            if self.get_magic_barrier() <= 0:
                self.get_battle().get_display().add_info('Enemy broke your magic shield')
        else:
            self._health_points -= dmg


class Rouge(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 20, 7, 11, 'rouge', display)
        self._agility = 20

    def get_agility(self):
        return self._agility

    def life_stealing_blade_attack(self, enemy: Enemy):
        self.get_battle().round(enemy, self.get_power()//2, self.get_speed() + self.get_agility() // 10)
        self.heal(self.get_power()//4)

    def fast_attack(self, enemy: Enemy):
        self.get_battle().round(enemy, self.get_power(), self.get_speed() + self.get_agility()//10)

    def take_dmg(self, dmg: int):
        if random.randint(0, 101) > self.get_agility():
            self._health_points -= dmg
        else:
            self.get_battle().get_display().add_info(f'You took {dmg} points of damage')
