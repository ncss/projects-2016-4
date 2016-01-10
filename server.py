from template.render import render
from tornado.ncss import Server
from db.db import User

def get_login(response):
    return response.get_secure_cookie('username')

def login_check_decorator(fn):
    def inner(response,*args, **kwargs):
        username1 =  response.get_secure_cookie('username')
        if username1 is None:
            return response.redirect('/account/login')
        return fn(response, *args, **kwargs)
    return inner

def index_handler(response):
    logged_in = get_login(response)
    if logged_in is not None:
        response.write('Welcome, {}'.format(logged_in))
    else:
        response.write("Welcome to Placebook!")

def signup_handler(response):
    logged_in = get_login(response)
    if logged_in is not None:
        response.redirect('/')
    else:
        signup_page = render("register.html",{})
        response.write(signup_page)

def login_handler(response):
    logged_in = get_login(response)
    if logged_in is not None:
        response.redirect("/account/profile")
    else:
        login_page = render("login.html",{})
        response.write(login_page)
        # file = open('test_login_form.html')
        #response.write(file.read())

def search_handler(response):
    logged_in = get_login(response)
    response.write("Search")

def location_handler(response, id):
    logged_in = get_login(response)
    response.write("Location {}".format(id))

@login_check_decorator
def create_handler(response):
    logged_in = get_login(response)
    response.write("Create Location")

@login_check_decorator
def user_handler(response, username):
    logged_in = get_login(response)
    response.write("Profile {}".format(username))

@login_check_decorator
def profile_handler(response):
    logged_in = get_login(response)
    response.write("username: {}".format(logged_in))

def login_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    user = User.find(username)
    if user and username == user.username and password == user.password:
        response.set_secure_cookie('username', username)
        response.redirect("/")
    else:
        response.write('Incorrect username or password')

def signup_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    user = User.find(username)
    if not user and username and password:
        User.create(username, password, None, "james@ncss.com", None, None)
        response.redirect("/account/login")
    else:
        response.write('Invalid something, could not create. Better error messages coming soon. ')

def logout_handler(response):
    response.clear_cookie("username")
    response.redirect("/")

@login_check_decorator
def location_creator(response):
    pass

if __name__ == '__main__':
    server = Server()
    server.register('/', index_handler)
    server.register("/account/signup",signup_handler, post=signup_authentication)
    server.register("/account/login", login_handler, post=login_authentication)
    server.register("/location/search", search_handler)
    server.register(r"/location/(\d+)", location_handler)
    server.register("/location/create", create_handler, post=location_creator)
    server.register("/account/profile/([a-z0-9A-Z._]+)", user_handler)
    server.register("/account/profile", profile_handler)
    server.register("/account/logout", logout_handler)
    server.run()
