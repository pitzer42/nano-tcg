from . import View


class LoginView(View):
    children = [
        'user_name_input',
        'login_button'
    ]

    def on_login(self, action):
        self.login_button.onclick = lambda _: action(self.user_name_input.value)

    def show(self):
        super(LoginView, self).show()
        self.user_name_input.focus()

    def login_error(self):
        self.user_name_input.classList.add('is-danger')
        self.user_name_input.classList.add('is-outlined')
        self.user_name_input.value = ''
        self.user_name_input.focus()
