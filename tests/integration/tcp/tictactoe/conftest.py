import pytest

from tictactoe.game_loop import game_loop


@pytest.fixture
def game_play():
    return game_loop
