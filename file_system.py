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
    player = o.player
    locations = o.locations

    pass


def map_json_deserializer(file):
    """
    Deserializes json into map object
    :param file: file content
    :return:
    """

    pass
