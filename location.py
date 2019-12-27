class Location:
    """
    This class defines basic properties and methods of a location
    """
    def __init__(self, loc_id, loc_type, loc_name, loc_description, locations, hidden_items=None, enemies=None):
        self._id = loc_id
        self._type = loc_type
        self._name = loc_name
        self._description = loc_description
        self._nearby_locations = []
        self._nearby_locations.extend(locations)
        self._hidden_items = [hidden_items]
        self._enemies = enemies

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
        self._nearby_locations.append((location_id, direction))

    @property
    def hidden_items(self):
        return self._hidden_items

    @hidden_items.deleter
    def hidden_items(self):
        del self._hidden_items

    @property
    def enemies(self):
        return self._enemies

    @enemies.deleter
    def enemies(self):
        del self._enemies

    def __str__(self):
        return self.description
