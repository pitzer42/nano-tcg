import json


def pack(command: str) -> bytes:
    return (command + '\n').encode()


def unpack(message: bytes) -> str:
    return message.decode().strip()


REQUEST_NAME = 'request_name'
REQUEST_DECK = 'request_deck'
END_DECK = 'end_deck'
REQUEST_MATCH = 'request_match'
REQUEST_MATCH_PASSWORD = 'request_match_password'
PROMPT_MULLIGAN = 'mulligan'
WAITING_OTHER_PLAYERS = 'waiting_other_players'
START = 'start'
MAIN_PHASE = 'main_phase'
SET_HAND = 'set_hand'
POSITIVES = ['', 'y', 'yes']


def prompt_mulligan(hand: list):
    return f'{PROMPT_MULLIGAN} {json.dumps(hand)}'


def is_positive(response: str):
    return response.lower() in POSITIVES


def set_hand(hand: list):
    return f'{SET_HAND} {json.dumps(hand)}'
