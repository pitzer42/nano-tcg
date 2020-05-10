from browser import console
from browser.websocket import WebSocket

COMMAND_ARGS_SEPARATOR = ' '


class WSEvents:

    def __init__(self, address):
        self._ws = WebSocket(address)
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

    def dispatch(self, event):

        console.log(event.data)

        command, args = self.parse(event.data)
        actions = self._events.get(command)
        if actions:
            if args:
                for action in actions:
                    action(args)
            else:
                for action in actions:
                    action()

    def parse(self, message: str) -> tuple:
        try:
            split_index = message.index(COMMAND_ARGS_SEPARATOR)
            command = message[:split_index]
            args = message[split_index + 1:]
        except ValueError:
            command = message
            args = None
        return command, args
