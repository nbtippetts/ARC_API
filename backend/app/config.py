#api/config.py
import urllib.parse
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY")
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009"))


class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009"))

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mariadb+pymysql://{}:{}@{}/{}'.format(
		os.getenv('DB_USER', 'flask'),
		os.getenv('DB_PASSWORD', ''),
		os.getenv('DB_HOST', 'mariadb'),
		os.getenv('DB_NAME', 'flask')
	)


env_config = {
	"development": DevelopmentConfig,
	"testing": TestingConfig,
	"production": ProductionConfig,
}
