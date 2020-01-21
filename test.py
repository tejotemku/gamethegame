from game import Game


def test_loading():
    game = Game()
    game.load_map("game save")
    assert game.map
