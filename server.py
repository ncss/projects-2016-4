from template.render import render
from tornado.ncss import Server
from db.db import User, Location, Rating, Tag
import hashlib
import re

def get_login(response):
    user_name = response.get_secure_cookie('username')
    if user_name:
        return user_name.decode()
    else:
        return None

def login_check_decorator(fn):
    def inner(response, *args, **kwargs):
        username1 = response.get_secure_cookie('username')
        if username1 is None:
            return response.redirect('/account/login')
        return fn(response, *args, **kwargs)
    return inner

def render_page(filename, response, context):
    context['logged_in'] = get_login(response)
    if context['logged_in']:
        user = User.find(context['logged_in'])
        context['user'] = user
    if 'query' not in context:
        context['query'] = None
    html = render(filename, context )
    response.write(html)

def index_handler(response):
    render_page('index.html', response, {})

def rating(response, location_id):
    if get_login(response):
        user_object = User.find(get_login(response))
        Rating.create(location_id, response.get_field('stars'), user_object.id)



def signup_handler(response):
    logged_in = get_login(response)
    context = {'error':None}
    if logged_in is not None:
        response.redirect('/')
    else:
        render_page('signup.html', response, context)


def login_handler(response):
    logged_in = get_login(response)
    context = {'login_error': None}
    if logged_in is not None:
        response.redirect("/account/profile")
    else:
        render_page('login.html', response, context)

def search_handler(response):
    context = {}
    results = []
    entry = response.get_field('search')
    if entry is None:
        response.redirect('/')
        return
    entry = entry.strip()
    context['query'] = entry
    if entry == '':
        response.redirect('/')
        return
    search_results = Location.search_name(entry)
    context['results'] = search_results
    render_page('searchresult.html', response, context)

def location_handler(response, id):
    location = Location.find_id(id)
    context = {}
    if location:
        context['location'] = location
        render_page('location.html', response, context)
    else:
        error_handler(response)


def error_handler(response):
    response.set_status(404)
    render_page('404.html', response, {})

@login_check_decorator
def create_handler(response):
    context = {'error': None}
    render_page('create_location.html', response, context)

@login_check_decorator
def edit_handler(response, location_id):
    context = {'error': None}
    location = Location.find_id(location_id)
    if location:
        context['location'] = location
        render_page('edit_location.html', response, context)
    else:
        error_handler(response)

def comment_handler(response):
    pass

def comment(response):
    comment = "This is a comment"


@login_check_decorator
def user_handler(response, username):
    response.write("Profile {}".format(username))

@login_check_decorator
def profile_handler(response):
    context = {}
    user_object = User.find(get_login(response))
    user_locations = Location.find_user_locations(user_object.id)
    context['results'] = user_locations
    render_page('account.html', response, context)

def login_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    user = User.find(username)
    context = {'login_error': None}
    if user and username == user.username and password == user.password:
        response.set_secure_cookie('username', username)
        response.redirect("/")
    else:
        context['login_error'] = 'Incorrect username or password'
        render_page("login.html", response, context)

def signup_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    c_password = response.get_field('confirm_password')
    fname = response.get_field('fname')
    lname = response.get_field('lname')
    email = response.get_field('email')
    user = User.find(username)
    context = {'error': None }
    if user:
        context["error"] = "Username taken"
    elif not username or not password or not email:
        context["error"] = "Username, password and email are required"
    elif password != c_password:
        context["error"] = "Passwords do not match"
    elif not re.match(r"^[0-9a-zA-Z_\.]+$", username):
        context["error"] = "Invalid username, please use only letters, numbers, underscores and periods"
    elif User.get_email(email) == email:
        context['error'] = "Email already taken"
    elif len(password) < 8:
        context["error"] = "Password must be at least 8 characters"
    else:
        User.create(username, password, None, email, fname, lname)
        response.set_secure_cookie('username', username)
        response.redirect("/")
        return None
    render_page('signup.html', response, context)


def logout_handler(response):
    response.clear_cookie("username")
    response.redirect("/")

@login_check_decorator
def location_creator(response):
    file_input = response.get_file('picture')
    filename_hash = hashlib.sha1(file_input[2]).hexdigest()

    file_output = open('./static/place-images/{}'.format(filename_hash), 'wb')
    file_output.write(file_input[2])
    file_output.close()

    context = {'error': None}

    name = response.get_field('name')
    description = response.get_field('description')
    address = response.get_field('address')
    username = get_login(response)
    user = User.find(username)

    try:
        lat = float(response.get_field('lat'))
        long = float(response.get_field('long'))
    except ValueError:
        context['error'] = 'Invalid latitude or longitude'
        render_page('create_location.html', response, context)
        return
    if Location.find_name(name):
        context['error'] = 'Place already exists'
        render_page('create_location.html', response, context)
    else:
        Location.create(name, description, filename_hash, user.id, address, lat, long)
        response.redirect("/location/{}".format(Location.find_name(name).id))

        tags = response.get_field('tags').split(',')
        if tags == ['']:
            tags = []
        for tag in tags:
            Tag.create_tag(tag, location.find_name(name).id)
    return

@login_check_decorator
def location_editor(response, id):
    #file_input = response.get_file('picture')
    #filename_hash = hashlib.sha1(file_input[2]).hexdigest()

    #file_output = open('./static/place-images/{}'.format(filename_hash), 'wb')
    #file_output.write(file_input[2])
    #file_output.close()

    context = {'error': None}

    name = response.get_field('name')
    description = response.get_field('description')
    address = response.get_field('address')
    username = get_login(response)
    user = User.find(username)

    try:
        lat = float(response.get_field('lat'))
        long = float(response.get_field('long'))
    except ValueError:
        context['error'] = 'Invalid latitude or longitude'
        render_page('create_location.html', response, context)
        return
    if Location.find_name(name):
        context['error'] = 'Place already exists'
        render_page('create_location.html', response, context)
    else:
        Location.create(name, description, filename_hash, user.id, address, lat, long)
        response.redirect("/location/{}".format(Location.find_name(name).id))
    return


if __name__ == '__main__':
    server = Server()
    server.register(r'/', index_handler)
    server.register(r"/account/signup",signup_handler, post=signup_authentication)
    server.register(r"/account/login", login_handler, post=login_authentication)
    server.register(r"/location/search", search_handler)
    server.register(r"/location/(\d+)", location_handler, post=rating)
    server.register(r'/comment', comment_handler, post=comment)
    server.register(r"/location/create", create_handler, post=location_creator)
    server.register(r"/location/edit/(\d+)", edit_handler, post=location_editor)
    server.register(r"/account/profile/([a-z0-9A-Z._]+)", user_handler)
    server.register(r"/account/profile", profile_handler)
    server.register(r"/account/logout", logout_handler)
    server.register(r"/.*", error_handler)
    server.run()
