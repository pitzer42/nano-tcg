import json

INITIAL_HAND_SIZE = 7

REQUEST_PLAYER_ID = 'request_name'
REQUEST_DECK = 'request_deck'
END_DECK = 'end_deck'
REQUEST_MATCH = 'request_match'
REQUEST_MATCH_PASSWORD = 'request_match_password'
PROMPT_MULLIGAN = 'mulligan'
WAITING_OTHER_PLAYERS = 'waiting_other_players'
START = 'start'
MAIN_PHASE = 'main_phase'
SET_HAND = 'set_hand'
REQUEST_PLAY = 'request_play'
SET_BOARD = 'set_board'
POSITIVES = ['', 'y', 'yes']


def prompt_mulligan(hand: list):
    return f'{PROMPT_MULLIGAN} {json.dumps(hand)}'


def set_hand(hand: list):
    return f'{SET_HAND} {json.dumps(hand)}'


def set_board(board: list):
    return f'{SET_BOARD} {json.dumps(board)}'


def is_positive(response: str):
    return response.lower() in POSITIVES
