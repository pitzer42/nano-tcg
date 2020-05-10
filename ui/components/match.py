from ui.components import Component


class MatchView(Component):
    _match_input = 'matchInput'
    _match_password_input = 'matchPasswordInput'
    _match_buton = 'matchButton'

    def __init__(self, document):
        super(MatchView, self).__init__(document)
        self._input = document[MatchView._match_input]
        self._password_input = document[MatchView._match_password_input]
        self._ok = document[MatchView._match_buton]
        self._first_try = True

    def get_match(self):
        return self._input.value

    def get_password(self):
        return self._password_input.value

    def set_ok_action(self, action):
        self._ok.bind(
            'click',
            action
        )

    def show(self):
        super(MatchView, self).show()
        if not self._first_try:
            self._input.classList.add('is-danger')
            self._input.classList.add('is-outlined')
        self._first_try = False
        self._input.value = ''
        self._password_input.value = ''
