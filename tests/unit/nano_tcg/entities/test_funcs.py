from gameplay.nano_magic.entities import draw


def test_draw():
    n = 1
    deck = [1, 2, 3]
    hand = []
    draw(n, deck, hand)
    assert deck == [1, 2]
    assert hand == [3]
