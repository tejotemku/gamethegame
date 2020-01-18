import json
from map import Map
from player import Rouge, Wizard, Knight
from location import Location, BattleLocation, Town


def map_json_serializer(o: Map):
    """
    Serializes map object to json so it can be saved
    :param o: map object
    :return:
    """

    locations = o.locations
    locations_table = []
    for loc in locations:
        locations_table.append(loc.get_dict())
    return json.dumps({
        'player': o.player.get_dict(),
        'locations': locations_table,
        'current location': o.current_location.id
    })


def map_json_deserializer(file):
    """
    Deserializes json into map object
    :param file: file content
    :return:
    """

    map_dict = json.load(file)

    player = map_dict.get('player')
    player_classes = {
        'knight': Knight,
        'wizard': Wizard,
        'rouge': Rouge
    }

    location_types = {
        'vanilla': Location,
        'town': Town,
        'battle': BattleLocation
    }

    locations_table = map_dict.get('locations')
    locations = []

    for loc in locations_table:
        locations.append(location_types.get(loc.get('type'))(loc))
    if player:
        return Map(
            locations=locations,
            cur_loc=map_dict.get('current location'),
            player=player_classes.get(player.get('class'))(player)
        )
    else:
        return Map(
            locations=locations,
            cur_loc=map_dict.get('current location')
        )
