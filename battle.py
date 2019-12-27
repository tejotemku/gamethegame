from gamedisplay import Display
import random


class Battle:
    def __init__(self, list_of_enemies, display: Display, game_map):
        self._player = game_map.player
        self._list_of_enemies = list_of_enemies
        self._rounds = 1
        self._display = display
        self._map = game_map
        self._reward_gold = 0
        self._reward_exp = 0

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
    def display(self):
        return self._display

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

    def round(self, list_of_targets, players_avatar):
        list_of_attacks_this_round = []
        for target in list_of_targets:
            list_of_attacks_this_round.append((target, players_avatar))

        for enemy in self._list_of_enemies:
            list_of_attacks_this_round.append((self.player, enemy))

        list_of_attacks_this_round = self.set_priority_of_attacks(list_of_attacks_this_round)

        for attack in list_of_attacks_this_round:
            if attack[0].check_if_alive() and attack[1].check_if_alive():
                self._display.add_info(f'{attack[1].name} attack {attack[0].name} for \
{attack[1].power} damage')
                attack[0].take_dmg(attack[1].power)

        for enemy in self.list_of_enemies:
            if enemy.check_if_alive():
                self.add_gold(enemy.rewards[1])
                self.add_exp(enemy.rewards[0])
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
            self.game_map.end_battle(self.player.check_if_alive(), self.exp, self.gold, items)

        self._rounds += 1

    def has_battle_ended(self):
        return self.player.hp <= 0 or not self.list_of_enemies

    @staticmethod
    def set_priority_of_attacks(attacks):
        for i in range(len(attacks)-1, 0, -1):
            for j in range(i):
                if attacks[i][1].speed > attacks[j][1].speed:
                    attacks[i], attacks[j] = attacks[j], attacks[i]
        return attacks
