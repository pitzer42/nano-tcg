import json

from browser import document, alert
from browser.websocket import WebSocket

from .views import swap_view, View
from .views.board import BoardView
from .views.login import LoginView
from .views.match_selector import MatchSelectorView

loading = View(document, template_id='LoadingView')
loading.show()

login = LoginView(document)

match_selector = MatchSelectorView(document)

board = BoardView(document)

ws = WebSocket('wss://nano0.0.0.0:8080/ws')  # ws = WebSocket('ws://0.0.0.0:8080/ws')


def on_ws_event(event):
    data = json.loads(event.data)
    print(f'{event}:{data}')
    if 'message' in data:
        message = data['message']
        if message == 'request_client_id':
            def send_user_name(user_name):
                json_response = json.dumps(dict(
                    client_id=user_name
                ))
                ws.send(json_response)
                swap_view(login, loading)

            login.on_login(send_user_name)
            swap_view(loading, login)
        elif message == 'alert_unavailable_player_id':
            login.login_error()
            swap_view(loading, login)
        elif message == 'request_match_id_and_password':
            options = data['options']
            match_selector.display_match_list(options)

            def join_match(match_id, match_password):
                json_response = json.dumps(dict(
                    match_id=match_id,
                    password=match_password
                ))
                ws.send(json_response)
                swap_view(match_selector, loading)

            match_selector.on_join(join_match)
            swap_view(loading, match_selector)
        elif message == 'sync':
            board.display(data['match']['board'])
            board.show()
            loading.hide()
        elif message == 'request_move':
            def send_play(index):
                print(index)
                print(data['options'][index])
                json_response = json.dumps(dict(
                    movement_index=index
                ))
                ws.send(json_response)

            board.enable_play(data['options'], send_play)
            board.show()
        elif message == 'notify_game_over':
            winner = data['winner']
            alert(f'{winner} won')


ws.bind('message', on_ws_event)
