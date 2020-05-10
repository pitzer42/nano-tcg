from browser.websocket import WebSocket

COMMAND_ARGS_SEPARATOR = ' '

class WSEvents:

    def __init__(self, address):
        self._ws = WebSocket(SERVER_ADDRESS)
        self._ws.bind(
            'message',
            self.dispatch)
        self._events = dict()

    def on(self, event, action):
        actions = self._events.get(event)
        if actions is None:
            actions = list()
            self._events[event] = actions
        actions.append(action)

    def dispatch(self, message: str):
        command, args = self.parse(message)
        actions = self._events.get(command_key)
        if actions:
            if args:
                for action in actions:
                    action(args)
            else:
                for action in actions:
                    action()

    def parse(self, message: str) -> tuple:
        try:
            split_index = event.data.index(COMMAND_ARGS_SEPARATOR)
            command = event.data[:split_index]
            args = event.data[split_index + 1:]
        except ValueError:
            command = event.data
            args = None
        return command, args





