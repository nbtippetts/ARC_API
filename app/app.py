from http.client import ImproperConnectionState
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from tzlocal import get_localzone
from datetime import datetime
import urllib.parse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import os


app = Flask(__name__)
api = Api(app)
tz = get_localzone()
print(tz)
LOCAL_DT = datetime.now()
print(LOCAL_DT)
LOCAL_DT = LOCAL_DT.replace(tzinfo=tz)
print(LOCAL_DT)

jobstores = {
	# 'default': SQLAlchemyJobStore(url="mysql+pymysql://root:{}@localhost/arc_db".format( urllib.parse.quote_plus("@Wicked2009")))
	'default': SQLAlchemyJobStore(url='mariadb+pymysql://{}:{}@{}/{}'.format(
		os.getenv('DB_USER', 'flask'),
		os.getenv('DB_PASSWORD', ''),
		os.getenv('DB_HOST', 'mariadb'),
		os.getenv('DB_NAME', 'flask')
	))
}
executors = {
	'default': ThreadPoolExecutor(20),
	'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
	'coalesce': False,
	'max_instances': 3
}

appscheduler = BackgroundScheduler(
	daemon=True, jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=tz)
appscheduler.start()
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://{}:{}@{}/{}'.format(
	os.getenv('DB_USER', 'flask'),
	os.getenv('DB_PASSWORD', ''),
	os.getenv('DB_HOST', 'mariadb'),
	os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)

class RoomModel(db.Model):
	__tablename__ = 'room'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	climate_schedule = db.relationship('ClimateScheduleModel', cascade='all, delete', backref='room',lazy='joined')
	climate_interval = db.relationship('ClimateIntervalModel', cascade='all, delete', backref='room',lazy='joined')
	climate = db.relationship('ClimateModel', cascade='all, delete', backref='room',lazy='joined')
	notebook = db.relationship('NoteBookModel', cascade='all, delete', backref='room', lazy='joined')
	ip = db.relationship('IPModel', cascade='all, delete', backref='room', lazy='joined')
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)

class IPModel(db.Model):
	__tablename__ = 'IP'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	state = db.Column(db.Boolean, default=False, nullable=False)
	ip = db.Column(db.String(20), default='False', nullable=False)
	climate_schedule = db.relationship('ClimateScheduleModel', cascade='all, delete',backref='IP', lazy='joined')
	climate_interval = db.relationship('ClimateIntervalModel', cascade='all, delete',backref='IP', lazy='joined')
	climate_schedule_log = db.relationship('ClimateScheduleLogModel', backref='IP', lazy='select', order_by='db.ClimateScheduleLogModel.end_time.desc()')
	climate = db.relationship('ClimateModel',cascade='all, delete', backref='IP', lazy='joined')
	climate_log = db.relationship('ClimateLogModel', backref='IP',lazy='select', order_by='db.ClimateLogModel.timestamp.desc()')
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)
class ClimateScheduleModel(db.Model):
	__tablename__ = 'climate_schedule'
	climate_schedule_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.String(100), nullable=False)
	end_time = db.Column(db.String(100), nullable=False)
	how_often = db.Column(db.String(20), nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)
class ClimateIntervalModel(db.Model):
	__tablename__ = 'climate_interval'
	climate_interval_id=db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable=False)
	interval_hour=db.Column(db.Integer, default=0, nullable=False)
	interval_minute=db.Column(db.Integer, default=0, nullable=False)
	duration_hour=db.Column(db.Integer, default=0, nullable = False)
	duration_minute=db.Column(db.Integer, default=0, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)

class ClimateModel(db.Model):
	__tablename__ = 'climate'
	climate_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	co2_parameters = db.Column(db.Integer, nullable=False)
	humidity_parameters = db.Column(db.Integer, nullable=False)
	temperature_parameters = db.Column(db.Integer, nullable=False)
	buffer_parameters = db.Column(db.Integer, default=0, nullable=False)
	co2_buffer_parameters = db.Column(db.Integer, default=0, nullable=False)
	co2_relay_ip = db.Column(db.String(20), nullable=False)
	humidity_relay_ip = db.Column(db.String(20), nullable=False)
	exhaust_relay_ip = db.Column(db.String(20), nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	climate_day_night = db.relationship(
		'ClimateDayNightModel', cascade='all, delete', backref='climate', lazy='joined')
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)
class ClimateDayNightModel(db.Model):
	__tablename__ = 'climate_day_night'
	id = db.Column(db.Integer, primary_key=True)
	climate_start_time = db.Column(db.Time, default=None)
	climate_end_time = db.Column(db.Time, default=None)
	climate_id = db.Column(db.Integer, db.ForeignKey('climate.climate_id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)

class ClimateScheduleLogModel(db.Model):
	__tablename__ = 'climate_schedule_log'
	climate_schedule_log_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.String(100), nullable=False)
	end_time = db.Column(db.String(100), nullable=False)
	end_time_flag = db.Column(db.Boolean, default=False, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)
class ClimateLogModel(db.Model):
	__tablename__ = 'climate_log'
	climate_log_id = db.Column(db.Integer, primary_key=True)
	co2 = db.Column(db.Integer, nullable=False)
	humidity = db.Column(db.Integer, nullable=False)
	temperature = db.Column(db.Integer, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class NoteBookModel(db.Model):
	__tablename__ = 'notebook'
	notebook_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	body = db.Column(db.String(800), nullable=False)
	publish_date = db.Column(db.String(100), nullable=False)
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)

from resources.arc_room import RoomIP, RoomList, IPList, IPLogs, AddIP
from resources.arc_schedule import RelaySchedule, RelayScheduleList, RoomRelayScheduleList
from resources.arc_interval import RelayInterval, RelayIntervalList, RoomRelayIntervalList
from resources.arc_climate import ClimateParameters, ClimateParametersIPList, ClimateParametersList, Climate, ClimateLog
from resources.arc_relay import RelayControl





# api.add_resource(Room, '/room/<int:room_id>')
api.add_resource(RoomList, '/rooms')

api.add_resource(AddIP, '/ip')
api.add_resource(RoomIP, '/room/<int:room_id>/ip/<int:ip_id>')
api.add_resource(IPLogs, '/room/<int:room_id>/ips')
api.add_resource(IPList, '/all_ips')

api.add_resource(RelayControl, '/relay_control/')

api.add_resource(RelaySchedule, '/room/<int:room_id>/relayschedule/<int:schedule_id>')
api.add_resource(RoomRelayScheduleList, '/room/<int:room_id>/relayschedule')
api.add_resource(RelayScheduleList, '/relayschedule')

api.add_resource(RelayInterval, '/room/<int:room_id>/relayinterval/<int:interval_id>')
api.add_resource(RoomRelayIntervalList, '/room/<int:room_id>/relayinterval')
api.add_resource(RelayIntervalList, '/relayinterval')

api.add_resource(ClimateParameters,'/room/<int:room_id>/climate/<int:climate_parameter_id>')
api.add_resource(ClimateParametersIPList, '/room/<int:room_id>/climate_ips')
api.add_resource(ClimateParametersList,'/room/<int:room_id>/climate')

api.add_resource(Climate, '/climate')
api.add_resource(ClimateLog, '/climate/log')

if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0')