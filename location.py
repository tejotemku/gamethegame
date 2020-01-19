from colorama import Fore


class Location:
    """
    This class defines basic properties and methods of a location
    """
    def __init__(self, loc):
        """
        This initiates a location object
        """
        self._id = loc.get('id')
        self._type = 'vanilla'
        self._name = loc.get('name')
        self._description = loc.get('description')
        self._nearby_locations = []
        if loc.get('locations'):
            self._nearby_locations.extend(loc.get('locations'))
        self._hidden_items = []
        if loc.get('hidden items'):
            self._hidden_items.extend(loc.get('hidden items'))
        self._key = loc.get('key')

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def nearby_locations(self):
        return self._nearby_locations

    def add_nearby_location(self, loc_id, loc_direction):
        """
        Adds nearby location where player will be able to go from this location
        :param loc_id: new location id
        :param loc_direction: How the direction to new location will be called
        """
        self._nearby_locations.append({
            'id': loc_id,
            'direction': loc_direction
        })

    def get_locations(self):
        for loc in self.nearby_locations:
            print(loc.get("direction"))

    @property
    def hidden_items(self):
        return self._hidden_items

    def find_hidden_items(self):
        items = self.hidden_items
        self._hidden_items = None
        return items

    @property
    def key(self):
        return self._key

    def open_location(self):
        """
        opens location
        """
        self._key = None

    def basic_commands(self):
        commands = {
            'look around': self.get_locations
        }
        return commands

    @staticmethod
    def help_command():
        print(f'{Fore.CYAN}look around{Fore.WHITE} - to find all possible directions you can go to')

    def __str__(self):
        return self.description

    def get_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'locations': self.nearby_locations,
            'hidden items': self.hidden_items,
            'key': self.key
        }


class Town(Location):
    def __init__(self, loc):
        super().__init__(loc=loc)
        self._type = 'town'

    def get_locations(self):
        super().get_locations()
        print('shop')


class BattleLocation(Location):
    def __init__(self, loc):
        super().__init__(loc=loc)
        self._enemies = loc.get('enemies')
        self._type = 'battle'

    @property
    def enemies(self):
        return self._enemies

    @enemies.setter
    def enemies(self, value):
        self._enemies = value

    def get_dict(self):
        loc_dict = super().get_dict()
        loc_dict.update({
                'enemies': self.enemies
            })
        return loc_dict
