from ui.components import Component


class LoginComponent(Component):
    _login_container = 'loginContainer'
    _name_input = 'nameInput'
    _login_button = 'loginButton'

    def __init__(self, document):
        super(LoginComponent, self).__init__(
            document,
            LoginComponent._login_container
        )
        self._name_input = document[LoginComponent._name_input]
        self._login_button = document[LoginComponent._login_button]
        self._first_try = True

    def get_user_name(self):
        return self._name_input.value

    def set_login_action(self, action):
        self._login_button.bind(
            'click',
            action
        )

    def show(self):
        super(LoginComponent, self).show()
        if not self._first_try:
            self._name_input.classList.add('is-danger')
            self._name_input.classList.add('is-outlined')
        self._first_try = False
        self._name_input.value = ''
