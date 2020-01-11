import random
from battle import Battle
from shop import Shop


class Player:
    """
    This is a class of a player
    """
    def __init__(self, name: str, hp_max: int, hp: int, speed: int, power: int, character_class: str,
                 exp: int = 0, lvl: int = 0, skill_points: int = 0, gold: int = 0, items=None, keys=None):
        """
        This method initiates a player object
        """
        # basic info
        self._name = name
        self._class = character_class
        self._battle = None
        # exp and gold
        self._experience = exp
        self._lvl = lvl
        self._skill_points = skill_points
        self._gold = gold
        # basic stats
        self._power = power
        self._speed = speed
        self._hp = hp
        self._hp_max = hp_max
        # locations keys
        self._keys = []
        if keys:
            self._keys.extend(keys)
        # items
        self._list_of_items = {}
        for i in Shop().items.keys():
            self.items.update({i: 0})
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
    def character_class(self):
        return self._class

    @property
    def battle(self):
        return self._battle

    @battle.setter
    def battle(self, new_battle: Battle):
        self._battle = new_battle

    # exp, lvl

    @property
    def exp(self):
        return self._experience

    def add_exp(self, new_exp: int):
        """
        Adds exp points
        """
        if new_exp > 0:
            self._experience += new_exp
            print(f'You have got new {new_exp} experience!')
        return self.level_up()

    def get_level(self):
        print(f'Level: {self.level}\nExp: {self.exp}\nYou need {int(10*pow(1.2, self.level))-self.exp} \
exp to level up\nSkill points: {self.skill_points}')

    @property
    def level(self):
        return self._lvl

    def level_up(self):
        """
        Level' up a player if requirements are met
        :return: if player leveled up
        """
        exp_to_level_up = int(10*pow(1.2, self.level))
        lvl_up = self.exp >= exp_to_level_up
        if lvl_up:
            self._lvl += 1
            self._experience -= exp_to_level_up
            print(f'You have leveled up! \nYou are currently on level {self.level}!\
            \nYou have got a skill point and now you have {self.skill_points}')
        return lvl_up

    @staticmethod
    def upgrade():
        print('You can upgrade one of the following:\npower\nspeed\nhp')

    @property
    def skill_points(self):
        return self._skill_points

    def remove_skill_point(self):
        self._skill_points -= 1

    def add_skill_point(self):
        self._skill_points += 1

    # gold methods

    def get_gold(self):
        print(f'{self.gold} gold')

    @property
    def gold(self):
        return self._gold

    def add_gold(self, gold):
        """
        adds gold to a player
        :param gold: acquired gold
        """
        if gold > 0:
            self._gold += gold
            print(f'You have earned {gold} gold!')

    def remove_gold(self, gold):
        """
        removes gold from a player if player has enough
        :param gold: removed gold
        :return: if player has enough gold
        """
        enough_gold = False
        if self._gold - gold >= 0:
            self._gold -= gold
            enough_gold = True
        return enough_gold

    # basic stats methods

    def get_stats(self):
        """
        :return: player's current stats
        """
        print(f'power: {self.power}\nspeed: {self.speed}\nhp: {self.hp}\nhp max: {self.hp_max}')

    @property
    def power(self):
        return self._power

    def power_increase(self):
        self._power += 1
        self.remove_skill_point()
        print(f'Increased your power up to {self.power}')

    @property
    def speed(self):
        return self._speed

    def speed_increase(self):
        self._speed += 1
        self.remove_skill_point()
        print(f'Increased your speed up to {self.speed}')

    @property
    def hp(self):
        return self._hp

    @property
    def hp_max(self):
        return self._hp_max

    def hp_increase(self):
        self._hp += 3
        self._hp_max += 3
        self.remove_skill_point()
        print(f'Increased your max hp up to {self.hp_max}')

    def heal(self, healed_hp_points):
        """
        Heals player by given number of points up to maximum health points
        :param healed_hp_points:
        :return:
        """
        hp = self.hp
        self._hp = min(self.hp + healed_hp_points, self.hp_max)
        print(f'You have been healed by {self.hp - hp} hp points')

    def check_if_alive(self):
        """
        :return:  Checks if player is alive
        """
        return self.hp > 0

    # keys&items methods
    def get_items(self):
        string = ''
        for i in self.items:
            string += f'i: {self.items.get(i)}\n'
        for k in self.keys:
            string += f'{k}\n'
        print(string[:-2])

    @property
    def items(self):
        return self._list_of_items

    def new_items(self, items):
        if items:
            for item in items:
                self.add_new_item(item)

    def add_new_item(self, item: str):
        """
        Adds items to player's inventory
        :param item:
        :return:
        """
        if self.items.keys().__contains__(item):
            self.items.update({item: self.items.get(item) + 1})
        else:
            self._keys.append(item)
        print(f'You have got new item, {item}!')

    def remove_item(self, item: str):
        has_item = False
        if self.items.__contains__(item):
            if self.items.get(item) > 0:
                self.items.update({item: self.items.get(item) - 1})
            has_item = True
            print(f'Used {item}')
        elif self.keys.__contains__(item):
            self.keys.remove(item)
            has_item = True
            print(f'Used {item}')
        return has_item

    @property
    def keys(self):
        return self._keys

    def basic_commands(self):
        commands = {
            'stats': self.get_stats,
            'gold': self.get_gold,
            'items': self.get_items,
            'level': self.get_level,
            'help': self.help_command
        }

        if self.items.get('small potion') > 0:
            commands.update({'small potion': [self.heal(10),
                            self.remove_item('small potion')]})

        if self.items.get('big potion') > 0:
            commands.update({'big potion': [self.heal(10),
                            self.remove_item('big potion')]})
        return commands

    @staticmethod
    def help_command():
        print('stats - to check your attributes\ngold - to check your gold\nitems - check your items\n\
level - check your level and exp\nsmall potion - to use potion if you have it\n\
big potion - to use potion if you have it')


class Knight(Player):
    """
    This is a subclass of a player that is a class of player's character class Knight
    """

    def __init__(self, name: str, hp_max: int = 40, hp: int = 40, speed: int = 5, power: int = 8,
                 ch_class: str = 'knight', exp: int = 0, lvl: int = 1, skill_points: int = 0,
                 gold: int = 0, items=None, keys=None):
        """
        This method creates object of Knight
        """
        super().__init__(name=name, hp_max=hp_max, hp=hp, speed=speed, power=power, character_class=ch_class, exp=exp,
                         lvl=lvl, skill_points=skill_points, gold=gold, items=items, keys=keys)
        # heavy armor of a knight reduces damage
        self.dmg_reduction = 2

    def hp_increase(self):
        self._hp += 5
        self._hp_max += 5

    def get_stats(self):
        """
        :return: player's current stats
        """
        print(super().get_stats() + f'\ndmg reduction: {self.dmg_reduction}')

    def normal_attack(self, enemy_id):
        """
        This is a method of knight's normal attack
        :param enemy_id: targeted enemy
        """
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.name, 10, 10, self.speed, self.power, 'attack avatar'))

    def heavy_attack(self, enemy_id):
        """
        This is a method of knight's heavy attack
        :param enemy_id: targeted enemy
        """
        if random.randint(0, 101) <= 85:
            self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                              Player(self.name, 10, 10, self.speed - 1, int(self.power*1.5), 'attack avatar'))
        else:
            print('You have missed the enemy')
            self.battle.round([], Player(self.name, 10, 10, self.speed, int(self.power*1.2), 'attack avatar'))

    def take_dmg(self, dmg: int):
        """
        Damages player by given damage, which is reduced by knight's damage reduction attribute
        :param dmg: damage that knight is hit with
        """
        print(f'Your heavy armor reduces {self.dmg_reduction} points of dmg')
        self._hp -= (dmg - self.dmg_reduction)

    @staticmethod
    def battle_help_command():
        print('normal attack <enemy id>- attacks chosen enemy with basic attack\n\
heavy attack - attacks chosen enemy with powerful heavy attack, but with lower speed and small chance to miss')


class Wizard(Player):
    """
    This is a subclass of a player that is a class of player's character class Knight
    """
    def __init__(self, name: str, hp_max: int = 18, hp: int = 18, speed: int = 7, power: int = 5,
                 ch_class: str = 'wizard', exp: int = 0, lvl: int = 1, skill_points: int = 0,
                 gold: int = 0, items=None, keys=None, magic_barrier: int = 4):
        super().__init__(name=name, hp_max=hp_max, hp=hp, speed=speed, power=power, character_class=ch_class, exp=exp,
                         lvl=lvl, skill_points=skill_points, gold=gold, items=items, keys=keys)
        self._magic_barrier = magic_barrier
        self._magic_barrier_max = magic_barrier

    def get_stats(self):
        """
        :return: player's current stats
        """
        super().get_stats()
        print(f'magic_barrier: {self._magic_barrier}')

    @property
    def magic_barrier(self):
        return self._magic_barrier

    @property
    def magic_barrier_max(self):
        return self._magic_barrier_max

    def reset_magic_barrier(self):
        self._magic_barrier = self._magic_barrier_max

    def magic_barrier_increase(self):
        self._magic_barrier_max += 1
        self.remove_skill_point()
        print(f'Increased your magic barrier up to {self.magic_barrier_max}')

    def aoe_attack(self):
        """
        This is a method of wizard's aoe attack
        """
        self.battle.round(self.battle.list_of_enemies, Player(self.name, 10, 10, self.speed, int(self.power*0.55),
                                                              'attack avatar'))

    def magic_attack(self, enemy_id):
        """
        This is a method of wizard's heavy attack
        :param enemy_id: targeted enemy
        """
        if random.randint(0, 101) <= 90:
            self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                              Player(self.name, 10, 10, self.speed, int(self.power*1.2), 'attack avatar'))
        else:
            print('You have missed the enemy')
            self.battle.round([], Player(self.name, 10, 10, self.speed, int(self.power*1.2), 'attack avatar'))

    def take_dmg(self, dmg: int):
        """
        Damages wizard's magic barrier and if it breaks it damages players health
        :param dmg: damage that wizard is hit with
        """
        if self.magic_barrier > 0:
            self._magic_barrier -= dmg
            print('Your magic barrier has absorbed damage')
            if self.magic_barrier <= 0:
                print('Enemy broke your magic barrier')
        else:
            self._hp -= dmg

    def upgrade(self):
        super().upgrade()
        print('magic barrier')

    @staticmethod
    def battle_help_command():
        print('magic attack <enemy id>- attacks chosen enemy with magic attack\n\
aoe - attacks every enemies in the battle')


class Rouge(Player):
    """
    This is a subclass of a player that is a class of player's character class Rouge
    """
    def __init__(self, name: str, hp_max: int = 20, hp: int = 20, speed: int = 7, power: int = 11,
                 ch_class: str = 'rouge', exp: int = 0, lvl: int = 1, skill_points: int = 0,
                 gold: int = 0, items=None, keys=None, agility: int = 20):
        super().__init__(name=name, hp_max=hp_max, hp=hp, speed=speed, power=power, character_class=ch_class, exp=exp,
                         lvl=lvl, skill_points=skill_points, gold=gold, items=items, keys=keys)
        self._agility = agility

    def get_stats(self):
        """
        :return: player's current stats
        """
        print(super().get_stats() + f'agility: {self.agility}')

    @property
    def agility(self):
        return self._agility

    def agility_increase(self):
        self._agility += 2
        self.remove_skill_point()
        print(f'Increased your agility up to {self.agility}')

    def upgrade(self):
        super().upgrade()
        print('\nagility')

    def life_stealing_blade_attack(self, enemy_id):
        """
        This is a method of rouge's life stealing attack, that damages enemy but also heals player
        :param enemy_id: targeted enemy
        """
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.name, 10, 10, self.speed + self.agility // 10, self.power//2, 'attack avatar'))
        self.heal(self.power//4)

    def fast_attack(self, enemy_id):
        """
        This is a method of rouge's fast attack
        :param enemy_id: targeted enemy
        """
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.name, 10, 10, self.speed + self.agility // 10, self.power, 'attack avatar'))

    def take_dmg(self, dmg: int):
        """
        Damages rouge hp by given damage, but first lets rouge dodge it
        :param dmg: damage that rouge is hit with
        """
        if random.randint(0, 101) > self.agility:
            self._hp -= dmg
        else:
            print(f'You took {dmg} points of damage')

    @staticmethod
    def battle_help_command():
        print('fast attack <enemy id>- attacks chosen enemy with quick attack\n\
life steal - attack chosen enemy and steals small amount of his hp healing player')
