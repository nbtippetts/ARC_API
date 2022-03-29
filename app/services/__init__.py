from flask import Flask
import urllib.parse
import os
from app.models import db

def create_app():
	app = Flask(__name__)
	# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009"))
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://{}:{}@{}/{}'.format(
		os.getenv('DB_USER', 'flask'),
		os.getenv('DB_PASSWORD', ''),
		os.getenv('DB_HOST', 'mariadb'),
		os.getenv('DB_NAME', 'flask')
	)
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.app_context().push()
	db.init_app(app)
	db.create_all()
	return app
