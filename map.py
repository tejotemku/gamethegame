from player import Player, Rouge, Wizard, Knight
from location import Location
from gamedisplay import Display
from battle import Battle


class Map:
    def __init__(self, name: str, player, starting_location: Location, display: Display):
        self._name = name
        self._player = player
        self._locations = [starting_location]
        self.game_state = 'explore'
        self._display = display
        self.battle = None

    def get_all_locations(self):
        return self._locations

    def add_location(self, location: Location):
        self.get_all_locations().append(location)

    def get_name(self):
        return self._name

    def get_player(self):
        return self._player

    def get_display(self):
        return self._display

    def get_game_state(self):
        return self.game_state

    def get_possible_directions(self):
        return self._locations[self.get_player().get_current_location()].get_nearby_locations()

    def move_to_different_location(self, location_id: int):
        self.get_player().move(location_id)
        # TODO make gui for locations

    def start_battle(self, list_of_enemies):
        self._player.set_battle(Battle(self._player, list_of_enemies, self.get_display()))
        self.game_state = 'battle'

    def end_battle(self, outcome, exp=0, reward=0, acquired_items=None):
        self.game_state = 'explore'
        # todo
        pass

    def handle_command(self, command: str):
        if self.get_game_state() == 'explore':
            pass
        else:
            player_class = self.get_player().get_class()
            if player_class == 'knight':
                if 'normal attack' in command:
                    self.get_player().normal_attack()
                elif 'heavy attack' in command:
                    self.get_player().heavy_attack()
                else:
                    self.get_display().add_info("Invalid command")
            if player_class == 'wizard':
                if 'aoe' in command:
                    self.get_player().aoe_attack()
                elif 'magic' in command:
                    self.get_player().magic_attack()
                else:
                    self.get_display().add_info('')
            if player_class == 'rouge':
                if 'life steal' in command:
                    self.get_player().life_stealing_blade_attack()
                elif 'fast attack' in command:
                    self.get_player().fast_attack()
                else:
                    self.get_display().add_info("Invalid command")


# Todo properties