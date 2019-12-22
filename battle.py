from gamedisplay import Display
from player import Player


class Battle:
    def __init__(self, player: Player, list_of_enemies, display: Display):
        self.player = player
        self.list_of_enemies = list_of_enemies
        self.rounds = 1
        self.display = display

    def round(self, list_of_targets, player_dmg, player_speed, player_name):
        list_of_attacks_this_round = []
        for target in list_of_targets:
            list_of_attacks_this_round.append((target, player_dmg, player_speed, player_name))

        for enemy in self.list_of_enemies:
            list_of_attacks_this_round.append((self.player, enemy.get_dmg(), enemy.get_speed(), enemy.get_name()))

        list_of_attacks_this_round = self.set_priority_of_attacks(list_of_attacks_this_round)

        for attack in list_of_attacks_this_round:
            self.display.add_info(f'{attack[3]} attack {attack[0].get_name()} for {attack[1]} damage')
            attack[0].take_dmg(attack[1])

        for enemy in self.list_of_enemies:
            if enemy.get_hp() <= 0:
                self.list_of_enemies.remove(enemy)

        battle_state = self.is_battle_won()
        # todo battle is won
        self.rounds += 1

    def is_battle_won(self):
        return self.rounds

    def get_display(self):
        return self.display

    @staticmethod
    def set_priority_of_attacks(list_of_attacks):
        for i in range(0, len(list_of_attacks)):
            for j in range(i + 1, len(list_of_attacks)):
                if list_of_attacks[i][2] < list_of_attacks[j][2]:
                    list_of_attacks[i], list_of_attacks[j] = list_of_attacks[j], list_of_attacks[i]
                    i = 0
                    j = 1

        return list_of_attacks

# Todo properties