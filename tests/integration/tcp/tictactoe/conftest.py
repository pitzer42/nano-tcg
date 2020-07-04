import pytest

from tictactoe.use_cases.game_loop import game_loop


@pytest.fixture
def game_play():
    return game_loop
