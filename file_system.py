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

    def knight_json_serializer(k: Knight):
        return {}

    def wizard_json_serializer(w: Wizard):
        return {
            'magic barrier': w.magic_barrier
        }

    def rouge_json_serializer(r: Rouge):
        return {
            'agility': r.agility
        }

    player_classes = {
        'knight': knight_json_serializer,
        'wizard': wizard_json_serializer,
        'rouge': rouge_json_serializer
    }

    player = o.player

    player_dict = {
            'name': player.name,
            'class': player.character_class,
            'level': player.level,
            'skill points': player.skill_points,
            'exp': player.exp,
            'gold': player.gold,
            'hp max': player.hp_max,
            'hp': player.hp,
            'power': player.power,
            'speed': player.speed,
            'items': player.items,
            'keys': player.keys
        }
    player_dict.update(player_classes.get(player.character_class)(player))

    def vanilla_loc_json_serializer(v: Location):
        return {}

    def town_loc_json_serializer(t: Town):
        return {}

    def battle_loc_serializer(b: BattleLocation):
        return {
            'enemies': b.enemies
        }

    location_types = {
        'vanilla': vanilla_loc_json_serializer,
        'town': town_loc_json_serializer,
        'battle': battle_loc_serializer
    }

    locations = o.locations
    locations_table = []
    for loc in locations:
        loc_dict = {
            'id': loc.id,
            'name': loc.name,
            'type': loc.type,
            'description': loc.description,
            'locations': loc.nearby_locations,
            'hidden items': loc.hidden_items,
            'key': loc.key
        }
        loc_dict.update(location_types.get(loc.type)(loc))
        locations_table.append(loc_dict)
    return json.dumps({
        'player': player_dict,
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

    def knight_json_deserializer(d: dict):
        return Knight(
            name=d.get('name'),
            ch_class=d.get('class'),
            lvl=d.get('level'),
            exp=d.get('exp'),
            gold=d.get('gold'),
            hp_max=d.get('hp max'),
            hp=d.get('hp'),
            power=d.get('power'),
            speed=d.get('speed'),
            items=d.get('items'),
            keys=d.get('keys'),
            skill_points=d.get('skill points')
        )

    def wizard_json_deserializer(d: dict):
        return Wizard(
            name=d.get('name'),
            ch_class=d.get('class'),
            lvl=d.get('level'),
            exp=d.get('exp'),
            gold=d.get('gold'),
            hp_max=d.get('hp max'),
            hp=d.get('hp'),
            power=d.get('power'),
            speed=d.get('speed'),
            items=d.get('items'),
            keys=d.get('keys'),
            skill_points=d.get('skill points'),
            magic_barrier=d.get('magic barrier')
        )

    def rouge_json_deserializer(d: dict):
        return Rouge(
            name=d.get('name'),
            ch_class=d.get('class'),
            lvl=d.get('level'),
            exp=d.get('exp'),
            gold=d.get('gold'),
            hp_max=d.get('hp max'),
            hp=d.get('hp'),
            power=d.get('power'),
            speed=d.get('speed'),
            items=d.get('items'),
            keys=d.get('keys'),
            skill_points=d.get('skill points'),
            agility=d.get('agility')
        )

    player = map_dict.get('player')
    player_classes = {
        'knight': knight_json_deserializer,
        'wizard': wizard_json_deserializer,
        'rouge': rouge_json_deserializer
    }

    def vanilla_loc_json_deserializer(d: dict):
        return Location(
            loc_id=d.get('id'),
            loc_name=d.get('name'),
            loc_description=d.get('description'),
            locations=d.get('locations'),
            hidden_items=d.get('hidden items'),
            key=d.get('key')
        )

    def town_loc_json_deserializer(d: dict):
        return Town(
            loc_id=d.get('id'),
            loc_name=d.get('name'),
            loc_description=d.get('description'),
            locations=d.get('locations'),
            hidden_items=d.get('hidden items'),
            key=d.get('key')
        )

    def battle_loc_deserializer(d: dict):
        return BattleLocation(
            loc_id=d.get('id'),
            loc_name=d.get('name'),
            loc_description=d.get('description'),
            locations=d.get('locations'),
            hidden_items=d.get('hidden items'),
            enemies=d.get('enemies'),
            key=d.get('key')
        )

    location_types = {
        'vanilla': vanilla_loc_json_deserializer,
        'town': town_loc_json_deserializer,
        'battle': battle_loc_deserializer
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
