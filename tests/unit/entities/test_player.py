from entities.player import Player


def test_create():
    expected_id = 42
    player = Player(expected_id)
    assert player.id == expected_id


def test_to_dict():
    id_key = 'id'
    expected_id = 42
    player = Player(expected_id)
    player_dict = player.to_dict()
    assert id_key in player_dict
    assert player_dict[id_key] == expected_id
