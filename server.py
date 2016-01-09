from tornado.ncss import Server

def index(response):
    response.write('Hello Team 4: Placebook!')

if __name__ == '__main__':
    server = Server()
    server.register('/', index)
    server.run()