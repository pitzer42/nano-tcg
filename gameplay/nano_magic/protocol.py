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
