#main.py
import os
from app.app import create_app

if __name__ == '__main__':
	app = create_app(os.getenv("FLASK_ENV"))
	app.run(app, host='0.0.0.0')
