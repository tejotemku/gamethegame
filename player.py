import random
from battle import Battle
from enemy import Enemy
from gamedisplay import Display
from shop import Shop


class Player:

    def __init__(self, name: str, hp: int, speed: int, power: int, character_class: str, display: Display):
        # basic info
        self._name = name
        self._current_location_id = 0
        self._class = character_class
        self._battle = None
        self._display = display
        # exp and gold
        self._experience = 0
        self._lvl = 1
        self._gold = 100
        # basic stats
        self._power = power
        self._speed = speed
        self._hp = hp
        self._hp_max = self._hp
        # items
        self._list_of_items = {}
        for key in Shop().items.keys():
            self._list_of_items.update({key: 0})

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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
        if new_exp > 0:
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
            self.display.add_info(f'You have leveled up! \nYou are currently on level {self.level}!\
            \nYou can upgrade one of the following:\npower\nspeed\nhp')
        return self.exp >= exp_to_level_up

    @property
    def gold(self):
        return self._gold

    def add_gold(self, gold):
        if gold > 0:
            self._gold += gold
            self.display.add_info(f'You have earned {gold} gold!')

    def remove_gold(self, gold):
        enough_gold = False
        if self._gold - gold >= 0:
            self._gold -= gold
            enough_gold = True
        return enough_gold

    # basic stats methods

    @property
    def power(self):
        return self._power

    def power_increase(self):
        self._power += 1

    @property
    def speed(self):
        return self._speed

    def speed_increase(self):
        self._speed += 1

    @property
    def hp(self):
        return self._hp

    @property
    def hp_max(self):
        return self._hp_max

    def hp_increase(self):
        self._hp += 3
        self._hp_max += 3

    def heal(self, healed_hp_points):
        self._hp = min(self.hp + healed_hp_points, self.hp_max)

    def check_if_alive(self):
        return self.hp > 0

    # items methods

    @property
    def list_of_items(self):
        return self._list_of_items

    def add_new_item(self, item: str):
        self.list_of_items.update({item: self.list_of_items.get(item) + 1})

    def remove_item(self, item: str):
        has_item = False
        if self.list_of_items.get(item) > 0:
            self.list_of_items.update({item: self.list_of_items.get(item) - 1})
            has_item = True
        return has_item

    def actions_in_battle(self):
        for item in ['big potion', 'small potion']:
            if item in self.list_of_items:
                self.display.add_info(f'use {item}')


class Knight(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 40, 5, 8, 'knight', display)
        # heavy armor of a knight reduces damage
        self.dmg_reduction = 2

    def hp_increase(self):
        self._hp += 5
        self._hp_max += 5

    def normal_attack(self, enemy):
        self.battle.round(enemy, Player(self.name, 10, self.speed, self.power, 'attack \
        avatar', self.display))

    def heavy_attack(self, enemy: Enemy):
        if random.randint(0, 101) <= 85:
            self.battle.round(enemy, Player(self.name, 10, self.speed - 1, int(self.power*1.5), 'attack \
        avatar', self.display))
        else:
            self.battle.get_display().add_info('You have missed the enemy')
            self.battle.round([], 0, 100, self.name)

    def actions_in_battle(self):
        super()
        self.display.add_info('normal attack\nheavy attack')

    def take_dmg(self, dmg: int):
        self._hp -= (dmg - self.dmg_reduction)


class Wizard(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 18, 7, 5, 'wizard', display)
        self._magic_barrier = 4

    @property
    def magic_barrier(self):
        return self._magic_barrier

    def magic_barrier_increase(self):
        self._magic_barrier += 1

    def aoe_attack(self):
        self.battle.round(self.battle.list_of_enemies, Player(self.name, 10, self.speed, int(self.power*0.55), 'attack \
        avatar', self.display))

    def magic_attack(self, enemy: Enemy):
        if random.randint(0, 101) <= 90:
            self.battle.round(enemy, Player(self.name, 10, self.speed, int(self.power*1.2), 'attack \
        avatar', self.display))
        else:
            self.battle.get_display().add_info('You have missed the enemy')
            self.battle.round([], 0, 100)

    def actions_in_battle(self):
        super()
        self.display.add_info('aoe attack\nmagic attack')

    def take_dmg(self, dmg: int):
        if self.magic_barrier > 0:
            self._magic_barrier -= dmg
            self.battle.get_display().add_info('Your magic barrier has absorbed damage')
            if self.magic_barrier <= 0:
                self.battle.get_display().add_info('Enemy broke your magic shield')
        else:
            self._hp -= dmg

    def level_up(self):
        lvl_up = super()
        if lvl_up:
            self.display.add_info('magic barrier')
        return lvl_up


class Rouge(Player):

    def __init__(self, name: str, display: Display):
        super().__init__(name, 20, 7, 11, 'rouge', display)
        self._agility = 20

    @property
    def agility(self):
        return self._agility

    def agility_increase(self):
        self._agility += 2

    def level_up(self):
        lvl_up = super()
        if lvl_up:
            self.display.add_info('agility')
        return lvl_up

    def life_stealing_blade_attack(self, enemy: Enemy):
        self.battle.round(enemy, Player(self.name, 10, self.speed + self.agility // 10, self.power//2, 'attack \
        avatar', self.display))
        self.heal(self.power//4)

    def fast_attack(self, enemy: Enemy):
        self.battle.round(enemy, Player(self.name, 10, self.speed + self.agility // 10, self.power, 'attack \
        avatar', self.display))

    def actions_in_battle(self):
        super()
        self.display.add_info('fast attack\nlife stealing attack')

    def take_dmg(self, dmg: int):
        if random.randint(0, 101) > self.agility:
            self._hp -= dmg
        else:
            self.battle.get_display().add_info(f'You took {dmg} points of damage')
