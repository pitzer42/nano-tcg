import pytest

from entities.match import Match


@pytest.fixture
def id_key():
    return 'expected_id'


@pytest.fixture
def expected_id():
    return 'expected_id'


@pytest.fixture
def expected_password():
    return 'expected_password'


@pytest.fixture
def match(expected_id, expected_password):
    return Match(
        expected_id,
        expected_password
    )


@pytest.fixture
def ready_match(match):
    player = 0
    while match.join(player):
        player += 1
    return match


def test_create(expected_id, expected_password):
    match = Match(
        expected_id,
        expected_password
    )
    assert match.id == expected_id


def test_join(match):
    assert match.join('player')


def test_cannot_join_more_players_than_its_size(ready_match):
    assert ready_match.is_ready()
    assert not ready_match.join('player')


def test_not_ready(match):
    assert not match.is_ready()


def test_yield_priority_changes_which_player_has_priority(ready_match):
    old_priority = ready_match.priority
    ready_match.yield_priority()
    assert not ready_match.has_priority(old_priority)
    assert old_priority != ready_match.priority


def test_successful_check_password(match, expected_password):
    assert match.check_password(expected_password)


def test_unsuccessful_check_password(match, expected_password):
    wrong_password = expected_password + expected_password
    assert not match.check_password(wrong_password)


def test_to_dict(match, id_key, expected_id):
    match_dict = match.to_dict()
    assert id_key in match_dict
    assert match_dict[id_key] == expected_id
