from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from board import create_app

if __name__ == '__main__':
    app = create_app()

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)

    # forks one process per cpu
    #http_server.bind(5000)
    #http_server.start(0)

    IOLoop.instance().start()
