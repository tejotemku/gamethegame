class Location:
    """
    This class defines basic properties and methods of a location

    Types of locations:
        1: Town - merchant and option to save the game
        2: Dungeons - has random enemy encounters
        3: Boss - Battle with powerful enemy
        4: Treasure - Basically
    """
    def __init__(self, loc_id, loc_type, loc_name, loc_description, parent_location_id, hidden_items):
        self._id = loc_id
        self._type = loc_type
        self._name = loc_name
        self._description = loc_description
        self._hidden_items = [hidden_items]
        self._nearby_locations = [parent_location_id, 'Return']

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_hidden_items(self):
        return self._hidden_items

    def get_nearby_locations(self):
        return self._nearby_locations

    def add_nearby_location(self, location):
        self._nearby_locations.append(location)

    def __str__(self):
        return self.get_description()
