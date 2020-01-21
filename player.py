import random
from battle import Battle
from shop import Shop
from colorama import Fore


class Player:
    """
    This is a class of a player
    """

    def __init__(self, character):
        """
        This method initiates a player object
        """
        # basic info
        self._name = character.get('name')
        self._class = character.get('class')
        self._battle = None
        # exp and gold
        self._experience = character.get('exp')
        self._lvl = character.get('level')
        self._skill_points = character.get('skill points')
        self._gold = character.get('gold')
        # basic stats
        self._power = character.get('power')
        self._speed = character.get('speed')
        self._hp = character.get('hp')
        self._hp_max = character.get('hp max')
        # locations keys
        self._keys = []
        if character.get('keys'):
            self._keys.extend(character.get('keys'))
        # items
        self._list_of_items = {}
        for i in Shop().items.keys():
            self.items.update({i: 0})
        if character.get('items'):
            for key in character.get('items'):
                self.items.update({key: character.get('items').get(key)})

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
        print(f'Level: {self.level}\nExp: {self.exp}\n\
You need {int(10*pow(1.2, self.level))-self.exp} \
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
            self.add_skill_point()
            print(
                f'You have leveled up! \nYou are currently on \
level {self.level}!')
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
        print(
            f'You have got a skill point and now you have {self.skill_points}')

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
        print(
            f'power: {self.power}\nspeed: {self.speed}\nhp: {self.hp}\n\
hp max: {self.hp_max}')

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
        print(f'You have got new item, {Fore.BLUE}{item}{Fore.WHITE}!')

    def remove_item(self, item: str):
        has_item = False
        if self.items.__contains__(item):
            if self.items.get(item) > 0:
                self.items.update({item: self.items.get(item) - 1})
                has_item = True
                print(f'Used {Fore.BLUE}{item}{Fore.WHITE}')
        elif self.keys.__contains__(item):
            self.keys.remove(item)
            has_item = True
            print(f'Used {Fore.BLUE}{item}{Fore.WHITE}')
        if not has_item:
            print(f'You don\'t have {Fore.BLUE}{item}{Fore.WHITE}')
        return has_item

    def small_potion(self):
        """
        uses small potion if player has one
        """
        if self.remove_item('small potion'):
            self.heal(10)

    def big_potion(self):
        """
        uses big potion if player has one
        """
        if self.remove_item('big potion'):
            self.heal(25)

    @property
    def keys(self):
        return self._keys

    def basic_commands(self):
        """
        :return: dictionary of basic commands that player can use
        """
        commands = {
            'stats': self.get_stats,
            'gold': self.get_gold,
            'items': self.get_items,
            'level': self.get_level,
            'small potion': self.small_potion,
            'big potion': self.big_potion
        }

        return commands

    @staticmethod
    def help_command():
        """
        lists commands that player can use always
        """
        print(f'{Fore.CYAN}stats{Fore.WHITE} - to check your attributes\n\
{Fore.CYAN}gold{Fore.WHITE} - to check your gold\n\
{Fore.CYAN}items{Fore.WHITE} - check your items\n\
{Fore.CYAN}level{Fore.WHITE} - check your level and exp \n\
{Fore.CYAN}upgrade{Fore.WHITE} - to upgrade on of yours attributes\n\
{Fore.CYAN}small potion{Fore.WHITE} - to use potion if you have it\n\
{Fore.CYAN}big potion{Fore.WHITE} - to use potion if you have it')

    def get_dict(self):
        return {
            'name': self.name,
            'class': self.character_class,
            'level': self.level,
            'skill points': self.skill_points,
            'exp': self.exp,
            'gold': self.gold,
            'hp max': self.hp_max,
            'hp': self.hp,
            'power': self.power,
            'speed': self.speed,
            'items': self.items,
            'keys': self.keys
        }


class Knight(Player):
    """
    This is a subclass of a player - Knight
    """

    def __init__(self, character):
        """
        This method creates object of Knight
        """
        super().__init__(character=character)
        # heavy armor of a knight reduces damage
        self.dmg_reduction = 2
        self._class = 'knight'

    def hp_increase(self):
        self._hp += 5
        self._hp_max += 5
        self.remove_skill_point()
        print(f'Increased your max hp up to {self.hp_max}')

    def get_stats(self):
        """
        :return: player's current stats
        """
        super().get_stats()
        print(f'dmg reduction: {self.dmg_reduction}')

    def normal_attack(self, enemy_id):
        """
        This is a method of knight's normal attack
        :param enemy_id: targeted enemy
        """
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(self.get_dict()))

    def heavy_attack(self, enemy_id):
        """
        This is a method of knight's heavy attack
        :param enemy_id: targeted enemy
        """
        player_dict = self.get_dict()
        player_dict.update({
            'power': int(self.power*1.5),
            'speed': int(self.speed) - 1
        })

        if random.randint(0, 101) <= 85:
            self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                              Player(player_dict))
        else:
            print('You have missed the enemy')
            self.battle.round([], Player(player_dict))

    def take_dmg(self, dmg: int):
        """
        Damages player by given damage, which is reduced by knight's damage \
reduction attribute
        :param dmg: damage that knight is hit with
        """
        print(f'Your heavy armor reduces {self.dmg_reduction} points of dmg')
        self._hp -= (dmg - self.dmg_reduction)

    @staticmethod
    def battle_help_command():
        print(f'{Fore.CYAN}normal{Fore.WHITE} <enemy id>- attacks chosen enemy \
with basic attack\n\
{Fore.CYAN}heavy{Fore.WHITE} - attacks chosen enemy with powerful heavy \
attack, but with lower speed and small\
 chance to miss')


class Wizard(Player):
    """
    This is a subclass of a player - Wizard
    """

    def __init__(self, character):
        super().__init__(character=character)
        self._magic_barrier = character.get('magic barrier')
        self._magic_barrier_max = character.get('magic barrier')
        self._class = 'wizard'

    def get_stats(self):
        """
        :return: player's current stats
        """
        super().get_stats()
        print(f'magic barrier: {self._magic_barrier}')

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

        player_dict = self.get_dict()
        player_dict.update({
            'power': int(self.power * 0.55)
        })

        self.battle.round(self.battle.list_of_enemies, Player(player_dict))

    def magic_attack(self, enemy_id):
        """
        This is a method of wizard's heavy attack
        :param enemy_id: targeted enemy
        """

        player_dict = self.get_dict()
        player_dict.update({
            'power': int(self.power * 1.2)
        })

        if random.randint(0, 101) <= 90:
            self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                              Player(player_dict))
        else:
            print('You have missed the enemy')
            self.battle.round([], Player(self.get_dict()))

    def take_dmg(self, dmg: int):
        """
        Damages wizard's magic barrier and if it breaks it damages players \
health
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
        print(f'{Fore.CYAN}magic{Fore.WHITE} <enemy id>- attacks chosen enemy \
with magic attack\n\
{Fore.CYAN}aoe{Fore.WHITE} - attacks every enemies in the battle')

    def get_dict(self):
        player_dict = super().get_dict()
        player_dict.update({'magic barrier': self.magic_barrier})
        return player_dict


class Rouge(Player):
    """
    This is a subclass of a player - Rouge
    """

    def __init__(self, character):
        super().__init__(character=character)
        self._agility = character.get('agility')
        self._class = 'rouge'

    def get_stats(self):
        """
        :return: player's current stats
        """
        super().get_stats()
        print(f'agility: {self.agility}')

    @property
    def agility(self):
        return self._agility

    def agility_increase(self):
        self._agility += 2
        self.remove_skill_point()
        print(f'Increased your agility up to {self.agility}')

    def upgrade(self):
        super().upgrade()
        print('agility')

    def life_stealing_blade_attack(self, enemy_id):
        """
        This is a method of rouge's life stealing attack, that damages enemy \
but also heals player
        :param enemy_id: targeted enemy
        """
        player_dict = self.get_dict()
        player_dict.update({
            'speed': self.speed + self.agility // 10,
            'power': self.power//2
        })
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(player_dict))

        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(player_dict))
        self.heal(self.power//4)

    def fast_attack(self, enemy_id):
        """
        This is a method of rouge's fast attack
        :param enemy_id: targeted enemy
        """
        player_dict = self.get_dict()
        player_dict.update({'speed': self.speed + self.agility // 10})
        self.battle.round(self.battle.list_of_enemies[int(enemy_id) - 1],
                          Player(player_dict))

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
        print(f'{Fore.CYAN}fast{Fore.WHITE} <enemy id>- attacks chosen enemy \
with quick attack\n\
{Fore.CYAN}life steal{Fore.WHITE} <enemy id> - attack chosen enemy and steals \
small amount of his hp healing player')

    def get_dict(self):
        player_dict = super().get_dict()
        player_dict.update({'agility': self.agility})
        return player_dict
