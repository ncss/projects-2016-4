from template.render import render
from tornado.ncss import Server
from db.db import User, Location, Rating, Tag, Comment
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
    if 'tags' not in context:
        context['tags'] = None
    html = render(filename, context )
    response.write(html)


def index_handler(response):
    render_page('index.html', response, {})


def rating(response, location_id):
    if get_login(response):
        user_object = User.find(get_login(response))
        Rating(location_id, response.get_field('stars'), user_object.id).create()


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
        response.redirect('/account/profile')
    else:
        render_page('login.html', response, context)


def search_handler(response):
    context = {}
    entry = response.get_field('search')
    lat_field = response.get_field('latitude')
    long_field = response.get_field('longitude')
    if lat_field and long_field:
        lat = float(lat_field)
        long = float(long_field)
        context['user_loc'] = [lat, long]
    else:
        context['user_loc'] = None
    tags = response.get_field('tags')
    if entry:
        entry = entry.strip()
    context['query'] = entry
    context['tags'] = tags
    if tags == '':
        search_results = Location.search_name(entry)
    elif entry == '':
        search_results = Location.search_tag(tags)
    else:
        search_results = Location.search(tags, entry)
    if lat_field and long_field:
        search_results.sort(key=lambda x: x.distance_from(lat, long))
    context['results'] = search_results
    render_page('searchresult.html', response, context)


def location_handler(response, id):
    logged_in = get_login(response)
    context = {}
    user_object = User.find(get_login(response))
    location = Location.find_id(id)
    loc_tags = Tag.find_from_place(location.id)
    if logged_in:
        stars = location.get_user_rating(user_object.id)
        context['user_rating'] = stars
    if location:
        context['location'] = location
        context['loc_tags'] = loc_tags
        context['comments'] = Comment.find_place(location.id)
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


@login_check_decorator
def comment_post(response, location_id):
    user_object = User.find(get_login(response))
    comment = response.get_field('comment')
    Comment(user_object.id, comment, location_id).create()
    response.redirect('/location/' + location_id)


@login_check_decorator
def user_handler(response, username):
    response.write('Profile {}'.format(username))


@login_check_decorator
def profile_handler(response, username=None):
    if username is None:
        user_object = User.find(get_login(response))
    else:
        user_object = User.find(username)
        if user_object is None:
            error_handler(response)
            return
    context = {}
    user_locations = Location.find_user_locations(user_object.id)
    context['results'] = user_locations
    context['user_object'] = user_object
    render_page('account.html', response, context)


def login_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    user = User.find(username)
    context = {'login_error': None}
    if user and username == user.username and password == user.password:
        response.set_secure_cookie('username', username)
        response.redirect('/')
    else:
        context['login_error'] = 'Incorrect username or password'
        render_page('login.html', response, context)


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
        context['error'] = 'Username taken'
    elif not username or not password or not email:
        context['error'] = 'Username, password and email are required'
    elif password != c_password:
        context['error'] = 'Passwords do not match'
    elif not re.match(r'^[0-9a-zA-Z_\.]+$', username):
        context['error'] = 'Invalid username, please use only letters, numbers, underscores and periods'
    elif User.get_email(email) == email:
        context['error'] = 'Email already taken'
    elif len(password) < 8:
        context['error'] = 'Password must be at least 8 characters'
    else:
        User(username, password, None, email, fname, lname).create()
        response.set_secure_cookie('username', username)
        response.redirect('/')
        return None
    render_page('signup.html', response, context)


def logout_handler(response):
    response.clear_cookie('username')
    response.redirect('/')


def comment_handler():
    pass


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
        Location(name, description, filename_hash, user.id, address, long, lat).create()
        response.redirect('/location/{}'.format(Location.find_name(name).id))

        tags = response.get_field('tags').split(',')
        if tags == ['']:
            tags = []
        for tag in tags:
            Tag(tag, Location.find_name(name).id).create()
    return


@login_check_decorator
def location_editor(response, id):
    context = {'error': None}
    location = Location.find_id(id)
    orig_name = location.name
    context['location'] = location
    if location is None:
        context['error'] = 'Place does not exist'
        render_page('edit_location.html', response, context)
        return
    name = response.get_field('name')
    if orig_name != name:
        if Location.find_name(name):
            context['error'] = 'Place already exists'
            render_page('edit_location.html', response, context)
            return None

    description = response.get_field('description')
    address = response.get_field('address')
    Location.change_location(id, name, description, location.picture, address, location.latitude, location.longitude)
    response.redirect('/location/' + id)


if __name__ == '__main__':
    server = Server(hostname='0.0.0.0', port=8888)
    server.register(r'/', index_handler)
    server.register(r'/account/signup', signup_handler, post=signup_authentication)
    server.register(r'/account/login', login_handler, post=login_authentication)
    server.register(r'/location/search', search_handler)
    server.register(r'/location/(\d+)', location_handler, post=rating)
    server.register(r'/location/(\d+)/comment', comment_handler, post=comment_post)
    server.register(r'/location/create', create_handler, post=location_creator)
    server.register(r'/location/edit/(\d+)', edit_handler, post=location_editor)
    server.register(r'/account/profile/([a-z0-9A-Z._]+)', profile_handler)
    server.register(r'/account/profile', profile_handler)
    server.register(r'/account/logout', logout_handler)
    server.register(r'.*', error_handler)
    server.run()
