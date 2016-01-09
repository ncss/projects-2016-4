from tornado.ncss import Server

def index(response):
    response.write('Hello, World!')

if __name__ == '__main__':
    server = Server()
    server.register('/', index)
    server.run()