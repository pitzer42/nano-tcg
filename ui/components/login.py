from ui.components import Component


class LoginView(Component):
    name_input = 'nameInput'
    login_button = 'loginButton'

    def __init__(self, document):
        super(LoginView, self).__init__(document)
        self.name_input = document[LoginView.name_input]
        self.login_button = document[LoginView.login_button]
        self._first_try = True

    def get_name(self):
        return self.name_input.value

    def set_action(self, action):
        self.login_button.bind(
            'click',
            action
        )

    def show(self):
        super(LoginView, self).show()
        if not self._first_try:
            self.name_input.classList.add('is-danger')
            self.name_input.classList.add('is-outlined')
        self._first_try = False
        self.name_input.value = ''
        self.name_input.focus()
