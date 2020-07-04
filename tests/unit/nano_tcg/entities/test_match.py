import pytest

from nano_magic.entities.match import Match

from gloop.channels import MemoryChannel


@pytest.fixture
def right_password():
    return 123


@pytest.fixture
def match(right_password):
    return Match(
        'match_1',
        right_password,
        MemoryChannel()
    )


def test_check_password(match, right_password):
    wrong_password = right_password + right_password
    assert match.check_password(right_password)
    assert not match.check_password(wrong_password)


def test_match_is_ready_after_n_players_have_joined(match):
    for i in range(Match.PLAYERS_IN_MATCH):
        assert not match.is_ready
        player = f'player_{i}'
        match.join(player)
    assert match.is_ready

