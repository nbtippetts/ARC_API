from app.config import env_config
from email.policy import default
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from tzlocal import get_localzone
from datetime import datetime
import urllib.parse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler import events
import os
import logging

logging.basicConfig(filename='/tmp/log', level=logging.INFO,format='[%(asctime)s]: %(levelname)s : %(message)s')
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


api = Api()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
jobstores = {
		#  'default': SQLAlchemyJobStore(url="mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009")))
  		'default': SQLAlchemyJobStore(url='mariadb+pymysql://{}:{}@{}/{}'.format(
  			os.getenv('DB_USER', 'flask'),
  			os.getenv('DB_PASSWORD', ''),
  			os.getenv('DB_HOST', 'mariadb'),
  			os.getenv('DB_NAME', 'flask')
  		))
}
executors = {
    'default': ThreadPoolExecutor(20),
  		'processpool': ProcessPoolExecutor(10)
}
job_defaults = {
    'coalesce': True,
  		'max_instances': 5
}

tz = get_localzone()
print(tz)
LOCAL_DT = datetime.now()
print(LOCAL_DT)
LOCAL_DT = LOCAL_DT.replace(tzinfo=tz)
print(LOCAL_DT)
appscheduler = BackgroundScheduler(
    daemon=True, jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=tz)


def job_listener(event):
		logging.info(event)

appscheduler.add_listener(job_listener,
						events.EVENT_JOB_EXECUTED |
						events.EVENT_JOB_MISSED |
						events.EVENT_JOB_ERROR)


def create_app(config_name):
	import app.resources
	app = Flask(__name__)
	app.config.from_object(env_config["development"])
	# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009"))
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://{}:{}@{}/{}'.format(
		os.getenv('DB_USER', 'flask'),
		os.getenv('DB_PASSWORD', ''),
		os.getenv('DB_HOST', 'mariadb'),
		os.getenv('DB_NAME', 'flask')
	)
	api.init_app(app)

	db.init_app(app)
	db.app = app
	with app.app_context():
		from app.models import RoomModel, IPModel, ClimateLiveDataModel, ClimateScheduleModel, ClimateIntervalModel, ClimateModel, ClimateDayNightModel, ClimateScheduleLogModel, ClimateLogModel, NoteBookModel
		db.create_all()
	migrate.init_app(app, db)
	ma.init_app(app)
	cors.init_app(app)
	appscheduler.start()
	return app