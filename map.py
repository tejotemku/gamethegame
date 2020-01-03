from location import Location
from battle import Battle
from enemy import enemies


class Map:
    """
    This is a class of a game map
    """
    def __init__(self, locations, player=None):
        """
        This creates an instance of a map
        :param locations: array of location objects in map
        :param player: player object
        """
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
        """
        Adds a new location to the map
        :param location: new location object
        """
        self.locations.append(location)

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, new_game_state):
        self._game_state = new_game_state

    # movement related methods

    def move_to_different_location(self, location_id: int):
        """
        Changes curret location of a player
        :param location_id: locations player are moving into
        """
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
        """
        Lists on screen possible directions a player can go to from current location he is in
        """
        self.player.display.add_info('From here you can go: ')
        for (loc_id, loc_direction) in self.locations[self.player.current_location].nearby_locations:
            self.player.display.add_info(f'{self.locations[loc_id].name} - {loc_direction}')
        if self.locations[self.player.current_location].type == 'town':
            self.player.display.add_info('-Town Shop-')

    # battle methods

    def start_battle(self, list_of_enemies):
        """
        Starts a battle with enemies
        :param list_of_enemies: array of Enemy objects that player will fight with during battle
        """
        self._player.battle = Battle(list_of_enemies, self.player.display, self)
        self.game_state = 'battle'
        self.player.display.start_a_battle_string()

    def end_battle(self, outcome, exp=0, gold=0, acquired_items=None):
        """
        Ends battle
        :param outcome: True/False information if player won or not
        :param exp: number of exp that player gets as a reward
        :param gold: number of gold that player gets as a reward
        :param acquired_items: items that player can get as a reward
        """
        if outcome:
            self.player.display.add_info("----You have won!----")
            self.game_state = 'explore'
            self.player.add_gold(gold)
            for item in acquired_items:
                self.player.add_new_item(item)
            del self.locations[self.player.current_location].enemies
            if self.player.add_exp(exp):
                self.game_state = 'level up'
        else:
            self.game_state = 'game_over'
            self.player.display.notification_box('Game Over!', 5)
        pass
