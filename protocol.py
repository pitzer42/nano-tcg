def wrap_message(command: str) -> bytes:
    return (command + '\n').encode()


REQUEST_NAME = 'request_name'
