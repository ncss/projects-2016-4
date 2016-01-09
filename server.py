from tornado.ncss import Server

def index_handler(response):
    response.write('Hello Team 4: Placebook!')

def signup_handler(response):
    response.write('Sign Up')

def login_handler(response):
    response.write('Login')

def search_handler(response):
    response.write("Search")

def location_handler(response, id):
    response.write("Location {}".format(id))

def create_handler(response):
    response.write("Create Location")

def user_handler(response, username):
    response.write("Profile {}".format(username))

def profile_handler(response):
    response.write("Profile")

if __name__ == '__main__':
    server = Server()
    server.register('/', index_handler)
    server.register("/account/signup",signup_handler)
    server.register("/account/login", login_handler)
    server.register("/location/search", search_handler)
    server.register(r"/location/(\d+)", location_handler)
    server.register("/location/create", create_handler)
    server.register("/account/profile/([a-z0-9A-Z._]+)", user_handler)
    server.register("/account/profile", profile_handler)
    server.run()
