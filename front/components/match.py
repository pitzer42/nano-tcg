class MatchComponent:

    _match_container = 'matchContainer'
    _match_input = 'matchInput'
    _match_password_input = 'matchPasswordInput'
    _match_buton = 'matchButton'

    def __init__(self, doc):
        self._container = doc[MatchComponent._match_container]
        self._input = doc[MatchComponent._match_input]
        self._password_input = doc[MatchComponent._match_password_input]
        self._ok = doc[MatchComponent._match_buton]
        self._first_try = True
        self.hide()

    def get_match_name(self):
        return self._input.value

    def get_match_password(self):
        return self._password_input.value

    def set_ok_action(self, action):
        self._ok.bind(
            'click',
            action
        )

    def hide(self):
        self._container.style.display = 'none'

    def show(self):
        if not self._first_try:
            self._input.classList.add('is-danger')
            self._input.classList.add('is-outlined')
        self._first_try = False
        self._input.value = ''
        self._password_input.value = ''
        self._container.style.display = 'flex'
