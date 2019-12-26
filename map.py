from location import Location
from battle import Battle


class Map:
    def __init__(self, name: str, starting_location: Location):
        self._name = name
        self._player = None
        self._game_state = 'explore'
        self._locations = [starting_location]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, new_player):
        self._player = new_player

    @property
    def locations(self):
        return self._locations

    def add_location(self, location: Location):
        self.locations.append(location)

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, new_game_state):
        self._game_state = new_game_state

    # movement related methods

    def move_to_different_location(self, location_id: int):
        location = self.locations[location_id]
        self.player.current_location = location_id
        self.player.player.display.add_info(f'You have entered: {location.name}')
        self.player.display.add_info(location)
        if location.type == 'boss':
            self.list_possible_directions()
        # todo boss

    def list_possible_directions(self):
        self.player.display.add_info('From here you can go: ')
        if self.locations[self.player.current_location].type == 'town':
            self.player.display.add_info('-Town Shop-')
        for (loc_id, loc_direction) in self.locations[self.player.current_location].nearby_locations:
            self.player.display.add_info(f'{self.locations[loc_id].name} - {loc_direction}')

    # battle methods

    def start_battle(self, list_of_enemies):
        self._player.set_battle(Battle(list_of_enemies, self.player.display, self))
        self.game_state = 'battle'
        self.player.display.start_a_battle()

    def end_battle(self, outcome, exp=0, reward=0, acquired_items=None):
        if outcome:
            self.game_state = 'explore'
            if self.player.add_exp(exp):
                self.game_state = 'level up'
            self.player.add_gold(reward)

        else:
            self.game_state = 'game_over'
            self.player.display.notification_box('Game Over!', 5)
        pass
