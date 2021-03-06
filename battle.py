from enemy import Enemy, enemies
import copy
import random
from colorama import Fore


class Battle:
    """
    This class represents an instance of a battle with one or more enemies
    """
    def __init__(self, list_of_enemies, game_map):
        """
        This initiates battle
        :param list_of_enemies: list of enemies in battle
        :param game_map: instance of map
        """
        self._player = game_map.player
        self._list_of_enemies = []
        if type(list_of_enemies) == Enemy:
            self._list_of_enemies = copy.deepcopy(enemies.get(list_of_enemies))
        else:
            for enemy in list_of_enemies:
                self._list_of_enemies.append(copy.deepcopy(enemies.get(enemy)))

        self._rounds = 1
        self._map = game_map
        self._reward_gold = 0
        self._reward_exp = 0
        self.start()

    @property
    def player(self):
        return self._player

    @property
    def list_of_enemies(self):
        return self._list_of_enemies

    @property
    def rounds(self):
        return self._rounds

    @property
    def game_map(self):
        return self._map

    @property
    def gold(self):
        return self._reward_gold

    def add_gold(self, value):
        self._reward_gold += value

    @property
    def exp(self):
        return self._reward_exp

    def add_exp(self, value):
        self._reward_exp += value

    def start(self):
        print('-------Battle starts!-------')
        self.list_enemies()

    def list_enemies(self):
        print(f'Round: {self.rounds}')
        for i, enemy in enumerate(self.list_of_enemies):
            print(f'{i+1}: {Fore.LIGHTMAGENTA_EX}{enemy.name}{Fore.WHITE} - \
                {enemy.hp} hp')

    def round(self, targets, players_avatar):
        """
        This method manages attacks during round of a battle
        :param targets: list of enemies that player will hit
        :param players_avatar: new temporary player instance that holds \
            modified power and speed value
        """
        list_of_attacks_this_round = []

        if type(targets) == Enemy:
            list_of_attacks_this_round.append((targets, players_avatar))
        else:
            for target in targets:
                list_of_attacks_this_round.append((target, players_avatar))

        for enemy in self._list_of_enemies:
            list_of_attacks_this_round.append((self.player, enemy))

        list_of_attacks_this_round = self.set_priority_of_attacks(
            list_of_attacks_this_round)

        for attack in list_of_attacks_this_round:
            if attack[0].check_if_alive() and attack[1].check_if_alive():
                print(f'{Fore.LIGHTGREEN_EX}{attack[1].name}{Fore.WHITE}\
 attack {Fore.LIGHTRED_EX}{attack[0].name}\
{Fore.WHITE} for {attack[1].power} damage')
                attack[0].take_dmg(attack[1].power)

        for enemy in self.list_of_enemies:
            if not enemy.check_if_alive():
                self.add_gold(enemy.rewards[1])
                self.add_exp(enemy.rewards[0])
                print(f'{enemy.name} has been defeated')
                self.game_map.current_location.enemies = self.list_of_enemies
                self.list_of_enemies.remove(enemy)

        if self.has_battle_ended():
            items = []
            ran = random.randint(0, 101)
            if ran == 1:
                items.append('golden key')
            if 10 < ran < 35:
                items.append('small potion')
            if 55 < ran < 65:
                items.append('big potion')
            self.game_map.end_battle(self.player.check_if_alive(), self.exp,
                                     self.gold, items)
        else:
            self.list_enemies()
        self._rounds += 1

    def has_battle_ended(self):
        """
        :return: if battle has already ended or not
        """
        return self.player.hp <= 0 or not self.list_of_enemies

    @staticmethod
    def set_priority_of_attacks(attacks):
        """
        Sorts attacks by higher speed
        :param attacks: list of attacks in current round
        :return: list of attacks sorted by speed
        """
        for i in range(len(attacks)-1, 0, -1):
            for j in range(i):
                if attacks[i][1].speed > attacks[j][1].speed:
                    attacks[i], attacks[j] = attacks[j], attacks[i]
        return attacks
