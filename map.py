from location import Location
from battle import Battle
from enemy import enemies


class Map:
    def __init__(self, locations, player=None):
        self._player = player
        self._game_state = 'explore'
        self._locations = []
        self._locations.extend(locations)

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
        self.player.display.add_info(f'You have entered: {location.name}')
        self.player.display.add_info(location.description)
        if location.enemies:
            enemies_in_location = []
            for enemy in location.enemies:
                enemies_in_location.append(enemies.get(enemy))
            self.start_battle(enemies_in_location)

    def list_possible_directions(self):
        self.player.display.add_info('From here you can go: ')
        for (loc_id, loc_direction) in self.locations[self.player.current_location].nearby_locations:
            self.player.display.add_info(f'{self.locations[loc_id].name} - {loc_direction}')
        if self.locations[self.player.current_location].type == 'town':
            self.player.display.add_info('-Town Shop-')

    # battle methods

    def start_battle(self, list_of_enemies):
        self._player.battle = Battle(list_of_enemies, self.player.display, self)
        self.game_state = 'battle'
        self.player.display.start_a_battle()

    def end_battle(self, outcome, exp=0, reward=0, acquired_items=None):
        if outcome:
            self.player.display.add_info("----You have won!----")
            self.game_state = 'explore'
            self.player.add_gold(reward)
            for item in acquired_items:
                self.player.add_new_item(item)
            del self.locations[self.player.current_location].enemies
            if self.player.add_exp(exp):
                self.game_state = 'level up'
        else:
            self.game_state = 'game_over'
            self.player.display.notification_box('Game Over!', 5)
        pass
