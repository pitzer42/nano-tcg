from browser import document, console

from nano_magic.ui.components.board import BoardView
from nano_magic.ui.components import DeckView
from nano_magic.ui.components import LoginView
from nano_magic.ui.components.match import MatchView
from nano_magic.ui.components import MulliganView
from nano_magic.ui.components import PlayView
from nano_magic.ui.components.wait import WaitView
from nano_magic.ui import WSEvents

# SERVER_ADDRESS = 'wss://nano-tcg.herokuapp.com/ws'
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
    ws.send(deck)
    ws.send('end_deck')


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
    ws.send('no')


def show_mulligan_component(hand):
    wait_component.hide()
    mulligan_component.show(hand)


mulligan_component = MulliganView(document)
mulligan_component.set_mulligan_action(send_mulligan)
mulligan_component.set_keep_action(send_keep)


def set_hand(hand):
    wait_component.hide()
    board_view.set_board(hand)


board_view = BoardView(document)


def show_board(cards):
    board_view.set_board(cards)
    board_view.show()


playView = PlayView(document)


def play_dialog(options):
    wait_component.hide()
    playView.set_options(options)

    def on_choice(index):
        message = str(index)
        ws.send(message)
        playView.hide()

    def end_turn(event):
        message = '-1'
        ws.send(message)
        playView.hide()
        console.log(event)

    playView.on_pass = end_turn
    playView.on_choice = on_choice
    playView.show()


events = WSEvents(SERVER_ADDRESS)

events.on('request_name', login_component.show)
events.on('request_deck', deck_component.show)
events.on('request_match', match_component.show)
events.on('request_match_password', send_match_password)
events.on('waiting_other_players', wait_component.show)
events.on('mulligan', show_mulligan_component)
events.on('start', console.log)
events.on('request_play', play_dialog)
events.on('set_board', show_board)

ws = events._ws  # TODO fix
