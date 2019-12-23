from location import Location
from gamedisplay import Display
from battle import Battle


class Map:
    def __init__(self, name: str, starting_location: Location, display: Display):
        self._name = name
        self._player = None
        self._locations = [starting_location]
        self._game_state = 'explore'
        self._display = display

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

    def get_all_locations(self):
        return self._locations

    def add_location(self, location: Location):
        self.get_all_locations().append(location)

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, new_game_state):
        self._game_state = new_game_state

    @property
    def display(self):
        return self._display

    # movement related methods

    def move_to_different_location(self, location_id: int):
        location = self.get_all_locations()[location_id]
        self.player().move(location_id)
        self.display.add_info(f'You have entered: {location.name}')
        self.display.add_info(location)
        if location.type not in ['boss', 'dungeon']:
            self.list_possible_directions()
        # todo boss'n'dungeon

    def list_possible_directions(self):
        self.display.add_info('From here you can go to: ')
        for (loc_id, loc_direction) in self.player().get_current_location().get_nearby_locations():
            self.display.add_info(f'{self.get_all_locations()[loc_id].name} - {loc_direction}')

    # battle methods

    def start_battle(self, list_of_enemies):
        self._player.set_battle(Battle(list_of_enemies, self.display, self))
        self.game_state = 'battle'

    def end_battle(self, outcome, exp=0, reward=0, acquired_items=None):
        if outcome:
            self.game_state = 'explore'
            if self.player().add_exp(exp):
                self.game_state = 'level up'
            self.player.add_gold(reward)

        else:
            self.game_state = 'game_over'
            self.display.notification_box('Game Over!', 5)
        pass
