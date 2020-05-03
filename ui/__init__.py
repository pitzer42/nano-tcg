from browser import alert, document, websocket

from ui.components.deck import DeckComponent
from ui.components.login import LoginComponent
from ui.components.match import MatchComponent
from ui.components.wait import WaitComponent
from ui.components.mulligan import MulliganComponent


def on_open(evt):
    pass


def on_message(evt):

    switch = {
        'request_name': login_component.show,
        'request_deck': deck_component.show,
        'request_match': match_component.show,
        'request_match_password': send_match_password,
        'waiting_other_players': wait_component.show
    }

    key = evt.data

    if key in switch:
        switch[key]()
    elif '[' in key:
        cards = list(key[2:-2].split("', '"))
        mulligan_component.set_hand(cards)
        mulligan_component.show()
        wait_component.hide()
    elif 'turn' in key:
        alert(key)


def on_close(evt):
    alert("Connection is closed")


def send_name(*args, **kwargs):
    name = login_component.get_user_name()
    ws.send(name)
    login_component.hide()


def send_deck(*args, **kwargs):
    deck_component.hide()
    deck = deck_component.get_deck()
    deck = deck.split('\n')
    for line in deck:
        ws.send(line)
    ws.send('end_deck')


def send_match(*args, **kwargs):
    name = match_component.get_match_name()
    ws.send(name)


def send_match_password(*args, **kwargs):
    password = match_component.get_match_password()
    ws.send(password)
    match_component.hide()

def send_mulligan(*args, **kwargs):
    ws.send('yes')

def send_keep(*args, **kwargs):
    ws.send('')

ws = websocket.WebSocket("ws://0.0.0.0:8080/ws")

ws.bind('open', on_open)
ws.bind('message', on_message)
ws.bind('close', on_close)

login_component = LoginComponent(document)
login_component.set_login_action(send_name)

deck_component = DeckComponent(document)
deck_component.set_deck_end_action(send_deck)

match_component = MatchComponent(document)
match_component.set_ok_action(send_match)

wait_component = WaitComponent(document)

mulligan_component = MulliganComponent(document)
mulligan_component.set_mulligan_action(send_mulligan)
mulligan_component.set_keep_action(send_keep)

