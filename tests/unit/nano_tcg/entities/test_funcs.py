from nano_magic.entities import draw, move


def test_draw():
    n = 1
    deck = ['1', '2', '3']
    hand = []
    draw(n, deck, hand)
    assert deck == ['1', '2']
    assert hand == ['3']


def test_move():
    i = 1
    hand = ['1', '2', '3']
    board = []
    move(i, hand, board)
    assert hand == ['1', '3']
    assert board == ['2']

