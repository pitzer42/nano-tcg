from browser import document, websocket, console

from ui.components.deck import DeckView
from ui.components.login import LoginView
from ui.components.match import MatchView
from ui.components.mulligan import MulliganView
from ui.components.wait import WaitView
from ui.events import WSEvents

SERVER_ADDRESS = 'ws://0.0.0.0:8080/ws'

events = WSEvents(SERVER_ADDRESS)

events.on('request_name', login_component.show)
events.on('request_deck', deck_component.show)
events.on('request_match', match_component.show)
events.on('request_match_password', send_match_password)
events.on('waiting_other_players', wait_component.show)
events.on('mulligan', show_mulligan_component)
events.on('start', console.log)
events.on('update_hand', console.log)
events.on('update_board', console.log)


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