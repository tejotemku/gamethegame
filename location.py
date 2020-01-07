class Location:
    """
    This class defines basic properties and methods of a location
    """
    def __init__(self, loc_id, loc_type, loc_name, loc_description, locations, hidden_items=None, enemies=None,
                 key=None):
        """
        This initiates a location object
        :param loc_id: id number
        :param loc_type: type of a location town/normal/boss/treasure
        :param loc_name: name
        :param loc_description: description
        :param locations: nearby locations that you can go to
        :param hidden_items: items hidden in this place
        :param enemies: enemies that player will encounter in this area
        :param key: key needed to enter this area
        """
        self._id = loc_id
        self._type = loc_type
        self._name = loc_name
        self._description = loc_description
        self._nearby_locations = []
        if locations:
            self._nearby_locations.extend(locations)
        self._hidden_items = []
        if hidden_items:
            self._hidden_items.extend(hidden_items)
        self._enemies = enemies
        self._key = key

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

    def add_nearby_location(self, location_id, direction):
        """
        Adds nearby location where player will be able to go from this location
        :param location_id: new location id
        :param direction: How the direction to new location will be called
        """
        self._nearby_locations.append((location_id, direction))

    @property
    def hidden_items(self):
        items = self._hidden_items
        self._hidden_items = None
        return items

    @property
    def enemies(self):
        return self._enemies

    @enemies.deleter
    def enemies(self):
        self._enemies = None

    @property
    def key(self):
        return self._key

    def open_location(self):
        """
        opens location
        """
        self._key = None

    def __str__(self):
        return self.description
