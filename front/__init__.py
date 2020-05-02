from browser import alert, document, websocket

from front.components.login import LoginComponent
from front.components.deck import DeckComponent
from front.components.match import MatchComponent
from front.components.wait import WaitComponent


def on_open(evt):
    pass


def on_message(evt):

    switch = {
        'request_name': login_component.show,
        'request_deck': deck_component.show,
        'request_match': match_component.show
    }

    key = evt.data

    if key in switch:
        switch[key]()


def on_close(evt):
    # websocket is closed
    alert("Connection is closed")


def send_name(*args, **kwargs):
    name = login_component.get_user_name()
    ws.send(name)
    login_component.hide()


def send_deck(*args, **kwargs):
    deck_component.hide()
    deck = deck_component.get_deck()
    deck = deck.split()
    for line in deck:
        ws.send(line)
    ws.send('end_deck')


def send_match(*args, **kwargs):
    match_component.hide()
    name = match_component.get_match_name()
    ws.send(name)
    password = match_component.get_match_password()
    ws.send(password)
    wait_component.show()


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
