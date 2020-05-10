from browser import document, websocket, console

from ui.components.deck import DeckView
from ui.components.login import LoginView
from ui.components.match import MatchView
from ui.components.mulligan import MulliganView
from ui.components.wait import WaitView

COMMAND_ARGS_SEPARATOR = ' '
SERVER_ADDRESS = 'ws://0.0.0.0:8080/ws'


def send_name(*args, **kwargs):
    login_component.hide()
    name = login_component.get_name()
    ws.send(name)


login_component = LoginView(document)
login_component.set_action(send_name)


def send_deck(*args, **kwargs):
    deck_component.hide()
    deck = deck_component.get_deck()
    deck += '\nend_deck'
    ws.send(deck)


deck_component = DeckView(document)
deck_component.set_action(send_deck)


def send_match(*args, **kwargs):
    match_component.hide()
    match = match_component.get_match()
    ws.send(match)


def send_match_password(*args, **kwargs):
    password = match_component.get_password()
    ws.send(password)


match_component = MatchView(document)
match_component.set_ok_action(send_match)

wait_component = WaitView(document)


def send_mulligan(*args, **kwargs):
    mulligan_component.hide()
    wait_component.show()
    ws.send('yes')


def send_keep(*args, **kwargs):
    mulligan_component.hide()
    wait_component.show()
    ws.send('')


def show_mulligan_component(hand):
    wait_component.hide()
    mulligan_component.show(hand)


mulligan_component = MulliganView(document)
mulligan_component.set_mulligan_action(send_mulligan)
mulligan_component.set_keep_action(send_keep)

COMMAND_SWITCH = {
    'request_name': login_component.show,
    'request_deck': deck_component.show,
    'request_match': match_component.show,
    'request_match_password': send_match_password,
    'waiting_other_players': wait_component.show,
    'mulligan': show_mulligan_component,
    'start': console.log,
    # 'update_hand': game_hand.show,
    # 'update_board': game_board.show,
}


def dispatch_command(event):
    try:
        split_index = event.data.index(COMMAND_ARGS_SEPARATOR)
        command_key = event.data[:split_index]
        args = event.data[split_index + 1:]
    except ValueError:
        command_key = event.data
        args = None

    command = COMMAND_SWITCH.get(command_key)
    if command:
        if args:
            command(args)
        else:
            command()

    console.log(f'{command_key}({type(args)})')


ws = websocket.WebSocket(SERVER_ADDRESS)
ws.bind('message', dispatch_command)
