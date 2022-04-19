#main.py
import os
from app.app import create_app
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

if __name__ == '__main__':
	app = create_app(os.getenv("FLASK_ENV"))
	http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
	http_server.serve_forever()
