import random
from battle import Battle
from enemy import Enemy
from gamedisplay import Display
from shop import Shop


class Player:

    def __init__(self, name: str, hp_max: int, hp: int, speed: int, power: int, character_class: str, display: Display,
                 current_location_id: int = 0, exp: int = 0, lvl: int = 0, gold: int = 0, items=None):
        # basic info
        self._name = name
        self._current_location_id = current_location_id
        self._class = character_class
        self._battle = None
        self._display = display
        # exp and gold
        self._experience = exp
        self._lvl = lvl
        self._gold = gold
        # basic stats
        self._power = power
        self._speed = speed
        self._hp = hp
        self._hp_max = hp_max
        # items
        self._list_of_items = {}
        for key in Shop().items.keys():
            self._list_of_items.update({key: 0})
        if items:
            for key in items:
                self.items.update({key: items.get(key)})

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
        lvl_up = self.exp >= exp_to_level_up
        if lvl_up:
            self._lvl += 1
            self._experience -= exp_to_level_up
            self.display.add_info(f'You have leveled up! \nYou are currently on level {self.level}!\
            \nYou can upgrade one of the following:\npower\nspeed\nhp')
        return lvl_up

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
    def items(self):
        return self._list_of_items

    def add_new_item(self, item: str):
        self.items.update({item: self.items.get(item) + 1})
        self.display.add_info(f'You have got new item, {item}!')

    def remove_item(self, item: str):
        has_item = False
        if self.items.get(item) > 0:
            self.items.update({item: self.items.get(item) - 1})
            has_item = True
        return has_item


class Knight(Player):

    def __init__(self, name: str, display: Display, hp_max: int = 40, hp: int = 40, speed: int = 5, power: int = 8,
                 ch_class: str = 'knight', current_location_id: int = 0, exp: int = 0, lvl: int = 1,
                 gold: int = 0, items=None):
        super().__init__(name, hp_max, hp, speed, power, ch_class, display, current_location_id, exp, lvl, gold, items)
        # heavy armor of a knight reduces damage
        self.dmg_reduction = 2

    def hp_increase(self):
        self._hp += 5
        self._hp_max += 5

    def normal_attack(self, enemy_id):
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.name, 10, 10, self.speed, self.power, 'attack avatar', self.display))

    def heavy_attack(self, enemy_id):
        if random.randint(0, 101) <= 85:
            self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                              Player(self.name, 10, 10, self.speed - 1, int(self.power*1.5), 'attack avatar',
                                     self.display))
        else:
            self.battle.display.add_info('You have missed the enemy')
            self.battle.round([], Player(self.name, 10, 10, self.speed, int(self.power*1.2), 'attack avatar',
                                         self.display))

    def take_dmg(self, dmg: int):
        self._hp -= (dmg - self.dmg_reduction)


class Wizard(Player):

    def __init__(self, name: str, display: Display, hp_max: int = 18, hp: int = 18, speed: int = 7, power: int = 5,
                 ch_class: str = 'wizard', current_location_id: int = 0, exp: int = 0, lvl: int = 1,
                 gold: int = 0, items=None, magic_barrier: int = 4):
        super().__init__(name, hp_max, hp, speed, power, ch_class, display, current_location_id, exp, lvl, gold, items)
        self._magic_barrier = magic_barrier

    @property
    def magic_barrier(self):
        return self._magic_barrier

    def magic_barrier_increase(self):
        self._magic_barrier += 1

    def aoe_attack(self):
        self.battle.round(self.battle.list_of_enemies, Player(self.name, 10, 10, self.speed, int(self.power*0.55),
                                                              'attack avatar', self.display))

    def magic_attack(self, enemy_id):
        if random.randint(0, 101) <= 90:
            self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                              Player(self.name, 10, 10, self.speed, int(self.power*1.2), 'attack avatar', self.display))
        else:
            self.battle.display.add_info('You have missed the enemy')
            self.battle.round([], Player(self.name, 10, 10, self.speed, int(self.power*1.2), 'attack avatar',
                                         self.display))

    def take_dmg(self, dmg: int):
        if self.magic_barrier > 0:
            self._magic_barrier -= dmg
            self.battle.display.add_info('Your magic barrier has absorbed damage')
            if self.magic_barrier <= 0:
                self.battle.display.add_info('Enemy broke your magic shield')
        else:
            self._hp -= dmg

    def level_up(self):
        lvl_up = super().level_up()
        if lvl_up:
            self.display.add_info('magic barrier')
        return lvl_up


class Rouge(Player):

    def __init__(self, name: str, display: Display, hp_max: int = 20, hp: int = 20, speed: int = 7, power: int = 11,
                 ch_class: str = 'rouge', current_location_id: int = 0, exp: int = 0, lvl: int = 1,
                 gold: int = 0, items=None, agility: int = 20):
        super().__init__(name, hp_max, hp, speed, power, ch_class, display, current_location_id, exp, lvl, gold, items)
        self._agility = agility

    @property
    def agility(self):
        return self._agility

    def agility_increase(self):
        self._agility += 2

    def level_up(self):
        lvl_up = super().level_up()
        if lvl_up:
            self.display.add_info('agility')
        return lvl_up

    def life_stealing_blade_attack(self, enemy_id):
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.name, 10, 10, self.speed + self.agility // 10, self.power//2, 'attack avatar',
                                 self.display))
        self.heal(self.power//4)

    def fast_attack(self, enemy_id):
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.name, 10, 10, self.speed + self.agility // 10, self.power, 'attack avatar',
                                 self.display))

    def take_dmg(self, dmg: int):
        if random.randint(0, 101) > self.agility:
            self._hp -= dmg
        else:
            self.battle.display.add_info(f'You took {dmg} points of damage')
