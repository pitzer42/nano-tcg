from tictactoe_ui.component import UIComponent


class MatchSelectorView(UIComponent):
    children = [
        'match_id_input',
        'match_password_input',
        'join_button',
        'match_list'
    ]

    def display_match_list(self, match_list):
        for match in match_list:
            list_item = self.doc.createElement('li')
            list_item.innerText = match
            self.match_list.appendChild(list_item)

    def on_join(self, action):
        self.join_button.onclick = lambda _: action(
            self.match_id_input.value,
            self.match_password_input.value,
        )
