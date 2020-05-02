class LoginComponent:

    _login_container = 'loginContainer'
    _name_input = 'nameInput'
    _login_button = 'loginButton'

    def __init__(self, doc):
        self._container = doc[LoginComponent._login_container]
        self._name_input = doc[LoginComponent._name_input]
        self._login_button = doc[LoginComponent._login_button]
        self._first_try = True
        self.hide()

    def get_user_name(self):
        return self._name_input.value

    def set_login_action(self, action):
        self._login_button.bind(
            'click',
            action
        )

    def hide(self):
        self._container.style.display = 'none'

    def show(self):
        if not self._first_try:
            self._name_input.classList.add('is-danger')
            self._name_input.classList.add('is-outlined')
        self._first_try = False
        self._name_input.value = ''
        self._container.style.display = 'flex'
