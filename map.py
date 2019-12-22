from player import Player
from location import Location


class Map:
    def __init__(self, name: str, player: Player, starting_location: Location):
        self._name = name
        self._player = player
        self._locations = [starting_location]
        self.game_state = 'explore'

    def get_all_locations(self):
        return self._locations

    def add_location(self, location: Location):
        self.get_all_locations().append(location)

    def get_name(self):
        return self._name

    def get_player(self):
        return self._player

    def get_possible_directions(self):
        return self._locations[self.get_player().get_current_location()].get_nearby_locations()

    def move_to_different_location(self, location_id: int):
        self.get_player().move(location_id)
        # TODO nigga make gui

    def handle_command(self, command: str):
        if self.game_state == 'explore':
            pass
        else:
            player_class = self.get_player().get_class()
            if player_class == 'rouge':
                pass