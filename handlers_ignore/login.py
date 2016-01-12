from db.db import User
from handlers.base import Handler


class LoginHandler(Handler):
    template_name = 'login'
    methods_allowed = ['GET', 'POST']

    def post_context(self):
        username = self.get_field('username')
        password = self.get_field('password')
        user = User.find(username)
        if user and username == user.username and password == user.password:
            self.set_secure_cookie('username', username)
            self.redirect('/')
        else:
            self.write('Incorrect username or password')