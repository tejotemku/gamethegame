from location import Location
from battle import Battle
from enemy import enemies


class Map:
    """
    This is a class of a game map
    """
    def __init__(self, locations, cur_loc, player=None):
        """
        This creates an instance of a map
        :param locations: array of location objects in map
        :param player: player object
        """
        self._player = player
        self._game_state = 'explore'
        self._locations = []
        self._locations.extend(locations)
        self._current_location = locations[cur_loc]

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, new_player):
        self._player = new_player

    @property
    def current_location(self):
        return self._current_location

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
    def move(self, command):
        for loc_id, loc_direction in self.current_location.nearby_locations:
            if self.compare_commands(loc_direction, command):
                if self.locations[loc_id].key:
                    if self.player.remove_item(self.locations[loc_id].key):
                        self.locations[loc_id].open_location()
                        print(f"You have opened: {self.locations[loc_id].name}")
                        self.move_to_different_location(loc_id)
                        return
                else:
                    self.move_to_different_location(loc_id)
                    return

    def move_to_different_location(self, location_id: int):
        """
        Changes curret location of a player
        :param location_id: locations player are moving into
        """
        self.current_location = self.locations[location_id]
        print(f'You have entered: {self.current_location.name}')
        print(self.current_location.description)

    # battle methods
    def start_battle(self, list_of_enemies):
        """
        Starts a battle with enemies
        :param list_of_enemies: array of Enemy objects that player will fight with during battle
        """
        self._player.battle = Battle(list_of_enemies, self)
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
            print("----You have won!----")
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

    @staticmethod
    def compare_commands(str1: str, str2: str):
        """
        :return: compares two strings by checking if one contains the other
        """
        return str1.lower() in str2.lower() or str2.lower() in str1.lower()