from gamedisplay import Display
from player import Player
from map import Map


class Battle:
    def __init__(self, list_of_enemies, display: Display, game_map: Map):
        self._player: Player = game_map.player
        self._list_of_enemies = list_of_enemies
        self._rounds = 1
        self._display = display
        self._map = game_map

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

    def round(self, list_of_targets):
        list_of_attacks_this_round = []
        for target in list_of_targets:
            list_of_attacks_this_round.append((target, self.player))

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
                self.list_of_enemies.remove(enemy)

        if self.has_battle_ended():
            self.game_map.end_battle(self.is_battle_won())

        self._rounds += 1

    def has_battle_ended(self):
        return self.player.health_points <= 0 or not self.list_of_enemies

    def is_battle_won(self):
        return self.player.health_points

    @staticmethod
    def set_priority_of_attacks(list_of_attacks):
        for i in range(0, len(list_of_attacks)):
            for j in range(i + 1, len(list_of_attacks)):
                if list_of_attacks[i][1].speed < list_of_attacks[j][1].speed:
                    list_of_attacks[i], list_of_attacks[j] = list_of_attacks[j], list_of_attacks[i]
                    i = 0
                    j = 1
        return list_of_attacks
