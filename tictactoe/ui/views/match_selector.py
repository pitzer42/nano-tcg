from . import View, fill_table


class MatchSelectorView(View):
    children = [
        'match_id_input',
        'match_password_input',
        'join_button',
        'match_table'
    ]

    def display_match_list(self, match_list):
        if len(match_list) > 0:
            fill_table(self.doc, match_list, table_element=self.match_table, id='ID')
            self.match_table.focus()

    def on_join(self, action):
        self.join_button.onclick = lambda _: action(
            self.match_id_input.value,
            self.match_password_input.value,
        )

    def show(self):
        super(MatchSelectorView, self).show()
        self.match_id_input.focus()
