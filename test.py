from game import Game
from location import Location


def test_loading():
    game = Game()
    game.load_map("game save")
    assert game.map


def test_location():
    dict_location = {
        "id": 33,
        "name": "Town",
        "type": "vanilla",
        "description": "test string",
        "hidden items": [],
        "locations": [],
        "key": None
    }
    location = Location(dict_location)
    assert location.id == 33
    assert location.name == "Town"
