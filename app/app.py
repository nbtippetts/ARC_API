from email.policy import default
from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from tzlocal import get_localzone
from datetime import datetime
import requests
import json
import urllib.parse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from apscheduler import events
from websocket import create_connection
import os
import logging

logging.basicConfig(filename='/tmp/log', level=logging.INFO,format='[%(asctime)s]: %(levelname)s : %(message)s')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://{}:{}@{}/{}'.format(
	os.getenv('DB_USER', 'flask'),
	os.getenv('DB_PASSWORD', ''),
	os.getenv('DB_HOST', 'mariadb'),
	os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)

jobstores = {
	# 'default': SQLAlchemyJobStore(url="mysql+pymysql://root:{}@localhost/arc_db".format(urllib.parse.quote_plus("@Wicked2009")))
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
	'coalesce': False,
	'max_instances': 5
}


tz = get_localzone()
print(tz)
LOCAL_DT = datetime.now()
print(LOCAL_DT)
LOCAL_DT = LOCAL_DT.replace(tzinfo=tz)
print(LOCAL_DT)
appscheduler = BackgroundScheduler(daemon=True, jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=tz)
def job_listener(event):
	logging.info(event)


appscheduler.add_listener(job_listener,
							events.EVENT_JOB_EXECUTED |
							events.EVENT_JOB_MISSED |
							events.EVENT_JOB_ERROR)
appscheduler.start()
# appscheduler.shutdown()

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
	climate_schedule_log = db.relationship('ClimateScheduleLogModel', backref='IP',lazy='select', order_by='ClimateScheduleLogModel.climate_schedule_log_id.desc()')
	climate = db.relationship('ClimateModel',cascade='all, delete', backref='IP', lazy='joined')
	climate_log = db.relationship('ClimateLogModel', backref='IP',lazy='select', order_by='ClimateLogModel.climate_log_id.desc()')
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


@app.before_first_request
def create_tables():
	db.create_all()

def get_local_time():
	local_tz = get_localzone()
	now_dt = datetime.now()
	now_local_dt = now_dt.replace(tzinfo=local_tz)
	local_time = now_local_dt.strftime("%I:%M %p")
	print(local_time)
	return local_time


def is_time_between(begin_time, end_time):
	local_tz = get_localzone()
	now_dt = datetime.now().time()
	now_local_dt = now_dt.replace(tzinfo=local_tz)
	if begin_time < end_time:
		return now_local_dt >= begin_time and now_local_dt <= end_time
	else:  # crosses midnight
		return now_local_dt >= begin_time or now_local_dt <= end_time

def start_task(*args):
	print(args)
	logging.info(args)
	ip_state = IPModel.query.filter_by(ip=args[1]).first()
	if ip_state.state == False:
		logs = ClimateScheduleLogModel(name=ip_state.name, start_time=get_local_time(), end_time=get_local_time(), end_time_flag=True, IP=ip_state)
		db.session.add(logs)
		db.session.commit()
		ip_state.state=True
		db.session.add(ip_state)
		db.session.commit()
		return args

def end_task(*args):
	print(args)
	logging.info(args)
	ip_state = IPModel.query.filter_by(ip=args[1]).first()
	logs = ClimateScheduleLogModel.query.filter_by(IP=ip_state).order_by(ClimateScheduleLogModel.climate_schedule_log_id.desc()).first()
	if logs.end_time_flag:
		logs.end_time_flag = False
		logs.end_time = get_local_time()
		db.session.add(logs)
		db.session.commit()
		ip_state.state = False
		db.session.add(ip_state)
		db.session.commit()
		return args


# def start_task(*args):
# 	print(args)
# 	url = f'http://{args[1]}/?v={args[0]}'
# 	res = requests.get(url,timeout=5)
# 	logging.info(res)
# 	if res.status_code == 200:
# 		ip_state = IPModel.query.filter_by(ip=args[1]).first()
# 		if ip_state.state == False:
# 			logs = ClimateScheduleLogModel(name=ip_state.name, start_time=get_local_time(), end_time=get_local_time(), end_time_flag=True, IP=ip_state)
# 			db.session.add(logs)
# 			db.session.commit()
# 			ip_state.state=True
# 			db.session.add(ip_state)
# 			db.session.commit()
# 			return res
# 	else:
# 		print(res)
# 		return res
# 	# print(url)
# def end_task(*args):
# 	print(args)
# 	url = f'http://{args[1]}/?v={args[0]}'
# 	res = requests.get(url,timeout=5)
# 	if res.status_code == 200:
# 		ip_state = IPModel.query.filter_by(ip=args[1]).first()
# 		logs = ClimateScheduleLogModel.query.filter_by(IP=ip_state).order_by(ClimateScheduleLogModel.climate_schedule_log_id.desc()).first()
# 		if logs.end_time_flag:
# 			logs.end_time_flag = False
# 			logs.end_time = get_local_time()
# 			db.session.add(logs)
# 			db.session.commit()
# 			ip_state.state = False
# 			db.session.add(ip_state)
# 			db.session.commit()
# 			return res
# 	else:
# 		print(res)
# 		return res

def check_ip_state(ip):
	end_task('high', ip.ip)
	ip.state = False
	db.session.add(ip)
	db.session.commit()
	return 'SUCCESS'


ip_marshaller = {
	'id': fields.Integer,
	"name": fields.String,
	"state": fields.Boolean,
	"ip": fields.String
}
climate_schedule_marshaller = {
	'climate_schedule_id': fields.Integer,
	'name': fields.String,
	'start_time': fields.String,
	'end_time': fields.String,
	"IP": fields.List(fields.Nested(ip_marshaller))
}

climate_interval_marshaller = {
	'climate_interval_id': fields.Integer,
	'name': fields.String,
	'interval_hour': fields.Integer,
	'interval_minute': fields.Integer,
	'duration_hour': fields.Integer,
	'duration_minute': fields.Integer,
	"IP": fields.List(fields.Nested(ip_marshaller))
}
climate_day_night_marshaller = {
	'id': fields.Integer,
	'climate_start_time': fields.String,
	'climate_end_time': fields.String,
	'climate_id': fields.Integer,
}

climate_marshaller = {
	'climate_id': fields.Integer,
	'name': fields.String,
	'buffer_parameters': fields.Integer,
	'co2_buffer_parameters': fields.Integer,
	'co2_parameters': fields.Integer,
	'humidity_parameters': fields.Integer,
	'temperature_parameters': fields.Integer,
	'co2_relay_ip': fields.String,
	'humidity_relay_ip': fields.String,
	'exhaust_relay_ip': fields.String,
	"climate_day_night": fields.List(fields.Nested(climate_day_night_marshaller))
}

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'climate_schedule': fields.Nested(climate_schedule_marshaller),
	'climate_interval': fields.Nested(climate_interval_marshaller),
	'climate': fields.Nested(climate_marshaller),
	'notebook': fields.Nested(climate_schedule_marshaller),
	'ip': fields.Nested(ip_marshaller),
}
# Define parser and request args
room_parser = reqparse.RequestParser()
room_parser.add_argument(
	'name', type=str, help='Please Name your Room', required=True)

class RoomList(Resource):
	@marshal_with(resource_fields)
	def get(self):
		rooms = RoomModel.query.all()
		if not rooms:
			abort(409, message="Rooms do not exist")
		return rooms, 200

class Room(Resource):
	@marshal_with(resource_fields)
	def get(self, room_id):
		results = RoomModel.query.filter_by(id=room_id).first()
		if results.climate:
			for climate in results.climate:
				if climate.climate_day_night:
					for climate_time in climate.climate_day_night:
						climate_time.climate_start_time = climate_time.climate_start_time.strftime("%I:%M %p")
						climate_time.climate_end_time = climate_time.climate_end_time.strftime("%I:%M %p")
						print(climate_time)

		return results, 200

	@marshal_with(resource_fields)
	def put(self, room_id):
		args = room_parser.parse_args()
		results = RoomModel.query.filter_by(id=room_id).first()
		if results:
			abort(409, message=f"Room {room_id} already exist")
		rooms = RoomModel(id=room_id, name=args['name'])
		db.session.add(rooms)
		db.session.commit()
		return rooms, 201

	@marshal_with(resource_fields)
	def patch(self, room_id):
		args = room_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} already exist".format(room_id))
		rooms.name = args['name']
		db.session.add(rooms)
		db.session.commit()
		return rooms, 201

	def delete(self, room_id):
		room = RoomModel.query.filter_by(id=room_id).first()
		if not room:
			abort(409, message="Room {} doesn't exist, cannot Delete.".format(room_id))
		db.session.delete(room)
		db.session.commit()
		return '', 204


climate_schedule_log_marshaller = {
	'climate_schedule_log_id': fields.Integer,
	'name': fields.String,
	'start_time': fields.String,
	'end_time': fields.String,
	'ip_id': fields.Integer,
}
climate_log_marshaller = {
	'climate_log_id': fields.Integer,
	'co2': fields.Integer,
	'humidity': fields.Integer,
	'temperature': fields.Integer,
	'ip_id': fields.Integer,
}

all_logs_resource_fields = {
	'id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'ip': fields.String,
	'climate_schedule_log':  fields.Nested(climate_schedule_log_marshaller),
	'climate_log':  fields.Nested(climate_log_marshaller),
}
logs_resource_fields = {
	'climate_schedule_log':  fields.Nested(climate_schedule_log_marshaller),
	'climate_log':  fields.Nested(climate_log_marshaller),
}
resource_fields = {
	'id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'ip': fields.String,
}
# Define parser and request args
ip_parser = reqparse.RequestParser()
ip_parser.add_argument('name', type=str, help='Invalid Name', required=False)
ip_parser.add_argument('IP', type=str, help='Invalid IP Address', required=True)


class IPList(Resource):
	@marshal_with(resource_fields)
	def get(self):
		results = IPModel.query.filter_by(room_id=None).all()
		if not results:
			abort(409, message="Room {} does not exist".format(results))
		return results, 200

class IPLogs(Resource):
	@marshal_with(logs_resource_fields)
	def get(self, room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))

		# ip_logs = IPModel.query.filter_by(room=rooms).all()
		climate_log = [p.climate_log[:5] for p in IPModel.query.filter_by(room=rooms).all() if p.climate_log]
		climate_schedule_log = [p.climate_schedule_log[:5] for p in IPModel.query.filter_by(room=rooms).all() if p.climate_schedule_log]

		return {'climate_log':climate_log, 'climate_schedule_log':climate_schedule_log}, 200


class RoomIP(Resource):
	@marshal_with(resource_fields)
	def get(self, room_id, ip_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		ips = IPModel.query.filter_by(id=ip_id, room=rooms).first()
		return ips, 200

	@marshal_with(resource_fields)
	def patch(self, room_id, ip_id):
		args = ip_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))

		ips = IPModel.query.filter_by(id=ip_id).first()
		if not ips:
			abort(409, message="IP {} doesn't exist, cannot update.".format(ip_id))
		# ips.name = args['name']
		ips.room_id = room_id
		db.session.add(ips)
		db.session.commit()
		return ips, 201

	def delete(self, room_id, ip_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		ips = IPModel.query.filter_by(id=ip_id, room=rooms).first()
		if not ips:
			abort(409, message="IP {} doesn't exist, cannot update.".format(ip_id))

		ips.room_id = None
		db.session.add(ips)
		db.session.commit()
		return '', 204

class AddIP(Resource):
	@marshal_with(resource_fields)
	def get(self):
		args = ip_parser.parse_args()
		print(args)
		ip_exists = IPModel.query.filter_by(ip=args['IP']).first()
		if ip_exists:
			return ip_exists, 201
		else:
			ip_name = args['name']
			print(ip_name)
			ip = IPModel(name=ip_name, ip=args['IP'])
			db.session.add(ip)
			db.session.commit()
			return ip, 201

class APJobInfo(Resource):
	# @marshal_with(resource_fields)
	def get(self):
		ap_job_list=[]
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			ap_job_list.append((job.id, job.trigger))

		return make_response(str(ap_job_list), 200)

resource_fields = {
	'climate_schedule_id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'start_time': fields.String,
	'end_time': fields.String,
	'ip_id': fields.Integer,
}
# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='What are you trying to create a schedule for?', required=False)
parser.add_argument('start_time', type=str, help='Invalid Date', required=True)
parser.add_argument('end_time', type=str, help='Invalid Date', required=True)
parser.add_argument('how_often', type=str, help='Invalid Interval', required=True)
parser.add_argument('ip_id', type=str, help='Invalid IP', required=False)


class RelayScheduleList(Resource):
	@marshal_with(resource_fields)
	def get(self):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)

		results = ClimateScheduleModel.query.all()
		return results, 200

class RoomRelayScheduleList(Resource):
	@marshal_with(resource_fields)
	def get(self,room_id):
		print(get_local_time())
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateScheduleModel.query.filter_by(room=rooms).all()
		return results, 200

class RelaySchedule(Resource):
	@marshal_with(resource_fields)
	def get(self,room_id,schedule_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateScheduleModel.query.filter_by(climate_schedule_id=schedule_id,room=rooms).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self,room_id,schedule_id):
		args = parser.parse_args()
		args['start_time']=datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M')
		args['end_time']=datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M')
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		ip_id = IPModel.query.filter_by(id=args['ip_id']).first()
		if not ip_id:
			abort(409, message="IP {} does not exist".format(ip_id))

		remove_ip = ClimateModel.query.filter(
			(ClimateModel.co2_relay_ip == ip_id.ip) |
			(ClimateModel.humidity_relay_ip == ip_id.ip) |
			(ClimateModel.exhaust_relay_ip == ip_id.ip)
		).first()
		if remove_ip:
			if remove_ip.co2_relay_ip == ip_id.ip:
				remove_ip.co2_relay_ip='False'
				if ip_id.state:
					check_ip_state(ip_id)
			if remove_ip.humidity_relay_ip == ip_id.ip:
				remove_ip.humidity_relay_ip='False'
				if ip_id.state:
					check_ip_state(ip_id)
			if remove_ip.exhaust_relay_ip == ip_id.ip:
				remove_ip.exhaust_relay_ip='False'
				if ip_id.state:
					check_ip_state(ip_id)

			db.session.add(remove_ip)
			db.session.commit()
		check_interval = ClimateIntervalModel.query.filter_by(IP=ip_id).first()
		if check_interval:
			start_job = appscheduler.get_job(f'{check_interval.climate_interval_id}-interval-start')
			if not start_job:
				abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(check_interval.climate_interval_id))

			end_job = appscheduler.get_job(f'{check_interval.climate_interval_id}-interval-end')
			if not end_job:
				abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(check_interval.climate_interval_id))

			appscheduler.remove_job(f'{check_interval.climate_interval_id}-interval-start')
			appscheduler.remove_job(f'{check_interval.climate_interval_id}-interval-end')
			db.session.delete(check_interval)
			db.session.commit()
			if ip_id.state:
				check_ip_state(ip_id)
		results = ClimateScheduleModel.query.filter_by(climate_schedule_id=schedule_id, IP=ip_id,room=rooms).first()
		if results:
			abort(409, message="Schedule {} already exist".format(schedule_id))
		start_display = args['start_time'].strftime("%I:%M %p")
		end_display = args['end_time'].strftime("%I:%M %p")
		schedule = ClimateScheduleModel(climate_schedule_id=schedule_id,
			name=args['name'], start_time=start_display, end_time=end_display, how_often=args['how_often'], IP=ip_id, room=rooms)

		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		start_triggers = CronTrigger(hour=start_hour, minute=start_minute)
		end_triggers = CronTrigger(hour=end_hour, minute=end_minute)
		appscheduler.add_job(start_task, start_triggers, id=f'{schedule_id}-start', args=['low', schedule.IP.ip], replace_existing=True)
		appscheduler.add_job(end_task, end_triggers, id=f'{schedule_id}-end', args=['high', schedule.IP.ip], replace_existing=True)
		return schedule, 201

	@marshal_with(resource_fields)
	def patch(self,room_id,schedule_id):
		args = parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		schedule = ClimateScheduleModel.query.filter_by(climate_schedule_id=schedule_id,room=rooms).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot update.".format(schedule_id))

		args['start_time']=datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M')
		args['end_time']=datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M')
		# schedule.name = args['name']
		schedule.start_time = args['start_time'].strftime("%I:%M %p")
		schedule.end_time = args['end_time'].strftime("%I:%M %p")
		schedule.how_often = args['how_often']
		if schedule.IP.state:
			check_ip_state(schedule.IP)
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		start_triggers = CronTrigger(hour=start_hour, minute=start_minute)
		end_triggers = CronTrigger(hour=end_hour, minute=end_minute)
		appscheduler.add_job(start_task, start_triggers, id=f'{schedule_id}-start', args=['low', schedule.IP.ip], replace_existing=True)
		appscheduler.add_job(end_task, end_triggers, id=f'{schedule_id}-end', args=['high', schedule.IP.ip], replace_existing=True)
		return 'Successfuly Updated', 204

	def delete(self,room_id,schedule_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		schedule = ClimateScheduleModel.query.filter_by(climate_schedule_id=schedule_id, room=rooms).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot Delete.".format(schedule_id))
		if schedule.name == "CO2":
			add_ip = ClimateModel.query.filter_by(co2_relay_ip='False').first()
			if add_ip:
				add_ip.co2_relay_ip = schedule.IP.ip
				db.session.add(add_ip)
				db.session.commit()
		if schedule.name == "Humidity":
			add_ip = ClimateModel.query.filter_by(humidity_relay_ip='False').first()
			if add_ip:
				add_ip.humidity_relay_ip = schedule.IP.ip
				db.session.add(add_ip)
				db.session.commit()
		if schedule.name == "Exhaust":
			add_ip = ClimateModel.query.filter_by(exhaust_relay_ip='False').first()
			if add_ip:
				add_ip.exhaust_relay_ip = schedule.IP.ip
				db.session.add(add_ip)
				db.session.commit()
		if schedule.IP.state:
			check_ip_state(schedule.IP)
		db.session.delete(schedule)
		db.session.commit()

		start_job = appscheduler.get_job(f'{schedule_id}-start')
		if not start_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(schedule_id))

		end_job = appscheduler.get_job(f'{schedule_id}-end')
		if not end_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(schedule_id))

		appscheduler.remove_job(f'{schedule_id}-start')
		appscheduler.remove_job(f'{schedule_id}-end')

		return 'SUCCESS', 204


resource_fields = {
	'climate_interval_id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'interval_hour': fields.Integer,
	'interval_minute': fields.Integer,
	'duration_hour': fields.Integer,
	'duration_minute': fields.Integer,
	'ip_id': fields.Integer,
}
# Define parser and request args
interval_parser = reqparse.RequestParser()
interval_parser.add_argument('name', type=str, help='What are you trying to create a schedule for?', required=False)
interval_parser.add_argument('interval_hour', type=int, help='Invalid Interval Hour', required=False)
interval_parser.add_argument('interval_minute', type=int,help='Invalid Interval Minute', required=False)
interval_parser.add_argument('duration_hour', type=int, help='Invalid Duration Hour', required=False)
interval_parser.add_argument('duration_minute', type=int,help='Invalid Duration Minute', required=False)
interval_parser.add_argument('ip_id', type=str, help='Invalid IP', required=False)


class RelayIntervalList(Resource):
	@marshal_with(resource_fields)
	def get(self):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)

		results = ClimateIntervalModel.query.all()
		return results, 200

class RoomRelayIntervalList(Resource):
	@marshal_with(resource_fields)
	def get(self,room_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateIntervalModel.query.filter_by(room=rooms).all()
		return results, 200

class RelayInterval(Resource):
	@marshal_with(resource_fields)
	def get(self,room_id,interval_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateIntervalModel.query.filter_by(climate_interval_id=interval_id,room=rooms).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self,room_id,interval_id):
		args = interval_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		ip_id = IPModel.query.filter_by(id=args['ip_id']).first()
		if not ip_id:
			abort(409, message="IP {} does not exist".format(ip_id))
		# db.session.add(ip_id)
		# db.session.commit()
		remove_ip = ClimateModel.query.filter(
			(ClimateModel.co2_relay_ip==ip_id.ip) |
			(ClimateModel.humidity_relay_ip==ip_id.ip) |
			(ClimateModel.exhaust_relay_ip==ip_id.ip)
		).first()
		if remove_ip:
			if remove_ip.co2_relay_ip == ip_id.ip:
				remove_ip.co2_relay_ip='False'
				if ip_id.state:
					check_ip_state(ip_id)
			if remove_ip.humidity_relay_ip == ip_id.ip:
				remove_ip.humidity_relay_ip='False'
				if ip_id.state:
					check_ip_state(ip_id)
			if remove_ip.exhaust_relay_ip == ip_id.ip:
				remove_ip.exhaust_relay_ip='False'
				if ip_id.state:
					check_ip_state(ip_id)

			db.session.add(remove_ip)
			db.session.commit()

		check_schedule = ClimateScheduleModel.query.filter_by(IP=ip_id).first()
		if check_schedule:
			start_job = appscheduler.get_job(
				f'{check_schedule.climate_schedule_id}-start')
			if not start_job:
				abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
					check_schedule.climate_schedule_id))

			end_job = appscheduler.get_job(f'{check_schedule.climate_schedule_id}-end')
			if not end_job:
				abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
					check_schedule.climate_schedule_id))

			appscheduler.remove_job(f'{check_schedule.climate_schedule_id}-start')
			appscheduler.remove_job(f'{check_schedule.climate_schedule_id}-end')
			db.session.delete(check_schedule)
			db.session.commit()
			if ip_id.state:
				check_ip_state(ip_id)


		results = ClimateIntervalModel.query.filter_by(climate_interval_id=interval_id, IP=ip_id,room=rooms).first()
		if results:
			abort(409, message="Interval {} already exist".format(interval_id))

		interval = ClimateIntervalModel(climate_interval_id=interval_id, name=args['name'], interval_hour=args['interval_hour'],interval_minute=args['interval_minute'],duration_hour=args['duration_hour'],duration_minute=args['duration_minute'], IP=ip_id, room=rooms)
		db.session.add(interval)
		db.session.commit()

		if args['interval_hour'] == 0:
			interval_hour='*'
		else:
			interval_hour=f"*/{str(args['interval_hour'])}"
		if args['interval_minute'] == 0:
			interval_minute='*'
		else:
			interval_minute=f"*/{str(args['interval_minute'])}"

		if args['duration_hour'] == 0:
			duration_hour = '*'
		else:
			duration_hour = f"*/{str(args['duration_hour'])}"
		if args['duration_minute'] == 0:
			duration_minute = '*'
		else:
			duration_minute = f"*/{str(args['duration_minute'])}"

		start_triggers = CronTrigger(hour=interval_hour, minute=interval_minute)
		end_triggers = CronTrigger(hour=duration_hour, minute=duration_minute)
		appscheduler.add_job(start_task,start_triggers,id=f'{interval_id}-interval-start',args=['low',interval.IP.ip],replace_existing=True)
		appscheduler.add_job(end_task,end_triggers,id=f'{interval_id}-interval-end',args=['high', interval.IP.ip], replace_existing=True)
		return interval, 201

	@marshal_with(resource_fields)
	def patch(self,room_id,interval_id):
		args = interval_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		interval = ClimateIntervalModel.query.filter_by(climate_interval_id=interval_id,room=rooms).first()
		if not interval:
			abort(409, message="Interval {} doesn't exist, cannot update.".format(interval_id))

		# schedule.name = args['name']
		interval.interval_hour = args['interval_hour']
		interval.interval_minute = args['interval_minute']
		interval.duration_hour = args['duration_hour']
		interval.duration_minute = args['duration_minute']
		if interval.IP.state:
			check_ip_state(interval.IP)
		db.session.add(interval)
		db.session.commit()

		if args['interval_hour'] == 0:
			interval_hour = '*'
		else:
			interval_hour = f"*/{str(args['interval_hour'])}"
		if args['interval_minute'] == 0:
			interval_minute = '*'
		else:
			interval_minute = f"*/{str(args['interval_minute'])}"

		if args['duration_hour'] == 0:
			duration_hour = '*'
		else:
			duration_hour = f"*/{str(args['duration_hour'])}"
		if args['duration_minute'] == 0:
			duration_minute = '*'
		else:
			duration_minute = f"*/{str(args['duration_minute'])}"
		start_triggers = CronTrigger(hour=interval_hour, minute=interval_minute)
		end_triggers = CronTrigger(hour=duration_hour, minute=duration_minute)
		appscheduler.add_job(start_task, start_triggers, id=f'{interval_id}-interval-start', args=['low', interval.IP.ip], replace_existing=True)
		appscheduler.add_job(end_task, end_triggers, id=f'{interval_id}-interval-end', args=['high', interval.IP.ip], replace_existing=True)
		return 'Successfuly Updated', 204

	def delete(self,room_id,interval_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		interval = ClimateIntervalModel.query.filter_by(climate_interval_id=interval_id, room=rooms).first()
		if not interval:
			abort(409, message="Interval {} doesn't exist, cannot Delete.".format(interval_id))
		if interval.name == "CO2":
			add_ip = ClimateModel.query.filter_by(co2_relay_ip='False').first()
			if add_ip:
				add_ip.co2_relay_ip = interval.IP.ip
				db.session.add(add_ip)
				db.session.commit()
		if interval.name == "Humidity":
			add_ip = ClimateModel.query.filter_by(humidity_relay_ip='False').first()
			if add_ip:
				add_ip.humidity_relay_ip = interval.IP.ip
				db.session.add(add_ip)
				db.session.commit()
		if interval.name == "Exhaust":
			add_ip = ClimateModel.query.filter_by(exhaust_relay_ip='False').first()
			if add_ip:
				add_ip.exhaust_relay_ip = interval.IP.ip
				db.session.add(add_ip)
				db.session.commit()
		if interval.IP.state:
			check_ip_state(interval.IP)
		db.session.delete(interval)
		db.session.commit()

		start_job = appscheduler.get_job(f'{interval_id}-interval-start')
		if not start_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(interval_id))

		end_job = appscheduler.get_job(f'{interval_id}-interval-end')
		if not end_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(interval_id))

		appscheduler.remove_job(f'{interval_id}-interval-start')
		appscheduler.remove_job(f'{interval_id}-interval-end')

		return 'SUCCESS', 204


climate_day_night_marshaller = {
	'id': fields.Integer,
	'climate_start_time': fields.String,
	'climate_end_time': fields.String,
	'climate_id': fields.Integer,
}

resource_fields = {
	'climate_id': fields.Integer,
	'room_id': fields.Integer,
	'name':fields.String,
	'buffer_parameters':fields.Integer,
	'co2_buffer_parameters':fields.Integer,
	'co2_parameters':fields.Integer,
	'humidity_parameters':fields.Integer,
	'temperature_parameters':fields.Integer,
	'co2_relay_ip':fields.String,
	'humidity_relay_ip':fields.String,
	'exhaust_relay_ip':fields.String,
	"climate_day_night": fields.List(fields.Nested(climate_day_night_marshaller))
}
climate_ips_resource_fields = {
	'id': fields.Integer,
	'ip': fields.String,
	'name':fields.String,
}

climate_parameters_parser = reqparse.RequestParser()
climate_parameters_parser.add_argument('name', type=str, help='Invalid Room', required=True)
climate_parameters_parser.add_argument('buffer_parameters', type=int, help='Invalid Buffer INT', required=True)
climate_parameters_parser.add_argument('co2_buffer_parameters', type=int, help='Invalid Buffer INT', required=True)
climate_parameters_parser.add_argument('co2_parameters', type=int, help='Invalid CO2 Data', required=True)
climate_parameters_parser.add_argument('humidity_parameters', type=int, help='Invalid Humidity Data', required=True)
climate_parameters_parser.add_argument('temperature_parameters', type=int, help='Invalid Temperature Data', required=True)
climate_parameters_parser.add_argument('climate_start_time', type=str, help='Invalid climate start date', required=False)
climate_parameters_parser.add_argument('climate_end_time', type=str, help='Invalid climate end date', required=False)
climate_parameters_parser.add_argument('co2_relay_ip', type=str, help='Invalid CO2 IP', required=True)
climate_parameters_parser.add_argument('humidity_relay_ip', type=str, help='Invalid Humidity IP', required=True)
climate_parameters_parser.add_argument('exhaust_relay_ip', type=str, help='Invalid Temperature IP', required=True)


class ClimateParametersIPList(Resource):
	@marshal_with(climate_ips_resource_fields)
	def get(self,room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		check_ips = IPModel.query.filter_by(room=rooms).all()
		valid_ips=[]
		ips_names = ['Exhaust','Humidity','CO2']
		for ips in check_ips:
			if ips.name in ips_names:
				valid_ips.append(ips)
		return valid_ips, 200

class ClimateParametersList(Resource):
	@marshal_with(resource_fields)
	def get(self,room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		climate = ClimateModel.query.filter_by(room=rooms).all()
		return climate, 200


class ClimateParameters(Resource):
	@marshal_with(resource_fields)
	def get(self,room_id, climate_parameter_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateModel.query.filter_by(climate_id=climate_parameter_id,room=rooms).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self,room_id,climate_parameter_id):
		args = climate_parameters_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		ips = IPModel.query.filter_by(name='Climate',room=rooms).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(ips))
		results = ClimateModel.query.filter_by(climate_id=climate_parameter_id, room=rooms).first()
		if results:
			abort(409, message="Climate {} already exist".format(climate_parameter_id))

		check_interval = ClimateIntervalModel.query.filter(
			ClimateIntervalModel.name.in_(['Exhaust', 'Humidity', 'CO2'])).all()
		if check_interval:
			for interval_id in check_interval:
				start_job = appscheduler.get_job(f'{interval_id.climate_interval_id}-interval-start')
				if not start_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(interval_id.climate_interval_id))

				end_job = appscheduler.get_job(f'{interval_id.climate_interval_id}-interval-end')
				if not end_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(interval_id.climate_interval_id))

				appscheduler.remove_job(f'{interval_id.climate_interval_id}-interval-start')
				appscheduler.remove_job(f'{interval_id.climate_interval_id}-interval-end')
				db.session.delete(interval_id)
				db.session.commit()
				if ips.state:
					check_ip_state(ips)
		check_schedule = ClimateScheduleModel.query.filter(
			ClimateScheduleModel.name.in_(['Exhaust', 'Humidity', 'CO2'])).all()
		if check_schedule:
			for schedule_id in check_schedule:
				start_job = appscheduler.get_job(f'{schedule_id.climate_schedule_id}-start')
				if not start_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(schedule_id.climate_schedule_id))

				end_job = appscheduler.get_job(f'{schedule_id.climate_schedule_id}-end')
				if not end_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(schedule_id.climate_schedule_id))

				appscheduler.remove_job(f'{schedule_id.climate_schedule_id}-start')
				appscheduler.remove_job(f'{schedule_id.climate_schedule_id}-end')
				db.session.delete(schedule_id)
				db.session.commit()
				if ips.state:
					check_ip_state(ips)

		climate = ClimateModel(
			climate_id=climate_parameter_id,
			name=args['name'],
			co2_parameters=args['co2_parameters'],
			humidity_parameters=args['humidity_parameters'],
			temperature_parameters=args['temperature_parameters'],
			buffer_parameters=args['buffer_parameters'],
			co2_buffer_parameters=args['co2_buffer_parameters'],
			co2_relay_ip=args['co2_relay_ip'],
			humidity_relay_ip=args['humidity_relay_ip'],
			exhaust_relay_ip=args['exhaust_relay_ip'],
			IP=ips, room=rooms
		)
		db.session.add(climate)
		db.session.commit()
		if args['climate_start_time'] is not None:
			climate_day_night = ClimateDayNightModel(
				climate_start_time=args['climate_start_time'],
				climate_end_time=args['climate_end_time'],
				climate=climate
			)
			db.session.add(climate_day_night)
			db.session.commit()
		return results, 201

	@marshal_with(resource_fields)
	def patch(self,room_id,climate_parameter_id):
		args = climate_parameters_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		climate = ClimateModel.query.filter_by(climate_id=climate_parameter_id, room=rooms).first()
		if not climate:
			abort(409, message="Climate Parameters {} doesn't exist, cannot update.".format(climate_parameter_id))

		check_interval = ClimateIntervalModel.query.filter(
			ClimateIntervalModel.name.in_(['Exhaust', 'Humidity', 'CO2'])).all()
		if check_interval:
			for interval_id in check_interval:
				start_job = appscheduler.get_job(
					f'{interval_id.climate_interval_id}-interval-start')
				if not start_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
						interval_id.climate_interval_id))

				end_job = appscheduler.get_job(
					f'{interval_id.climate_interval_id}-interval-end')
				if not end_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
						interval_id.climate_interval_id))

				appscheduler.remove_job(f'{interval_id.climate_interval_id}-interval-start')
				appscheduler.remove_job(f'{interval_id.climate_interval_id}-interval-end')
				if interval_id.IP.state:
					check_ip_state(interval_id.IP)

				db.session.delete(interval_id)
				db.session.commit()

		check_schedule = ClimateScheduleModel.query.filter(
			ClimateScheduleModel.name.in_(['Exhaust', 'Humidity', 'CO2'])).all()
		if check_schedule:
			for schedule_id in check_schedule:
				start_job = appscheduler.get_job(
					f'{schedule_id.climate_schedule_id}-start')
				if not start_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
						schedule_id.climate_schedule_id))

				end_job = appscheduler.get_job(
					f'{schedule_id.climate_schedule_id}-end')
				if not end_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
						schedule_id.climate_schedule_id))

				appscheduler.remove_job(f'{schedule_id.climate_schedule_id}-start')
				appscheduler.remove_job(f'{schedule_id.climate_schedule_id}-end')
				if schedule_id.IP.state:
					check_ip_state(schedule_id.IP)

				db.session.delete(schedule_id)
				db.session.commit()

		climate.co2_parameters = args['co2_parameters']
		climate.humidity_parameters = args['humidity_parameters']
		climate.temperature_parameters = args['temperature_parameters']
		climate.buffer_parameters = args['buffer_parameters']
		climate.co2_buffer_parameters = args['co2_buffer_parameters']
		climate.co2_relay_ip = args['co2_relay_ip']
		climate.humidity_relay_ip = args['humidity_relay_ip']
		climate.exhaust_relay_ip = args['exhaust_relay_ip']

		db.session.add(climate)
		db.session.commit()
		climate_day_night = ClimateDayNightModel.query.filter_by(climate=climate).first()
		if climate_day_night:
			climate_day_night.climate_start_time = args['climate_start_time'],
			climate_day_night.climate_end_time = args['climate_end_time'],
			db.session.add(climate_day_night)
			db.session.commit()

		return climate, 204

	def delete(self,room_id, climate_parameter_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		climate = ClimateModel.query.filter_by(climate_id=climate_parameter_id, room=rooms).first()
		if not climate:
			abort(409, message="climate {} doesn't exist, cannot Delete.".format(climate_parameter_id))
		db.session.delete(climate)
		db.session.commit()
		return 'SUCCESS', 204


climate_parser = reqparse.RequestParser()
climate_parser.add_argument('co2', type=int, help='Invalid CO2')
climate_parser.add_argument('humidity', type=float, help='Invalid Humidity')
climate_parser.add_argument('temperature', type=float, help='Invalid Temperature')

class Climate(Resource):
	def get(self):
		args = climate_parser.parse_args()
		print(args)

		# ips = IPModel.query.filter_by(ip='192.168.0.133').first()
		print(request.remote_addr)
		ips = IPModel.query.filter_by(ip=str(request.remote_addr)).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(request.remote_addr))
		try:
			# ws = create_connection(f"ws://10.42.0.1:8000/ws/socket-server/")
			# ws = create_connection(f"ws://127.0.0.1:8000/ws/socket-server/")
			ws = create_connection(f"ws://192.168.1.42:8000/ws/socket-server/")
			# ws = create_connection(f"ws://192.168.1.37:8000/ws/socket-server/")
			ws.send(json.dumps({"data": args, "room_id": str(ips.room_id)}))
			result = ws.recv()
			print("Received '%s'" % result)
			ws.close()
		except Exception as e:
			pass

		climate = ClimateModel.query.filter_by(IP=ips).all()
		if not climate:
			abort(409, message="Climate {} does not exist".format(1))
		for c in climate:
			climate_day_night = ClimateDayNightModel.query.filter_by(climate=c).first()
			if climate_day_night:
				check_time = is_time_between(
					climate_day_night.climate_start_time, climate_day_night.climate_end_time)
				print(check_time)
				if check_time:
					climate = c
				else:
					climate = ClimateModel.query.filter_by(IP=ips).first()


		co2_buffer = climate.co2_parameters+climate.co2_buffer_parameters
		humidity_plus = climate.humidity_parameters+climate.buffer_parameters
		humidity_minus = climate.humidity_parameters-climate.buffer_parameters
		temperature_buffer = climate.temperature_parameters+climate.buffer_parameters
		try:
			if climate.co2_relay_ip =='False':
				print('do nothing')
			else:
				if args['co2'] <= co2_buffer:
					start_task('low',climate.co2_relay_ip)
				elif args['co2'] >= co2_buffer:
					end_task('high', climate.co2_relay_ip)
				else:
					print('co2 do nothing')
		except Exception as e:
			pass

		try:
			if climate.exhaust_relay_ip == 'False':
				print('do nothing')
			else:
				if args['temperature'] >= temperature_buffer:
					start_task('low', climate.exhaust_relay_ip)
				elif args['temperature'] <= temperature_buffer and args['humidity'] >= humidity_plus:
					start_task('low', climate.exhaust_relay_ip)
				elif args['temperature'] <= temperature_buffer:
					end_task('high', climate.exhaust_relay_ip)
				else:
					print('temp do nothing')
		except Exception as e:
			pass
		try:
			if climate.humidity_relay_ip == 'False':
				print('do nothing')
			else:
				if args['humidity'] <= humidity_minus:
					start_task('low', climate.humidity_relay_ip)
				elif args['humidity'] >= humidity_minus:
					end_task('high', climate.humidity_relay_ip)
				else:
					print('humidity do nothing')

		except Exception as e:
			pass

		return 'SUCCESS', 200


class ClimateLog(Resource):
	def get(self):
		args = climate_parser.parse_args()
		print(args)
		# ips = IPModel.query.filter_by(ip='192.168.1.12').first()
		print(request.remote_addr)
		ips = IPModel.query.filter_by(ip=str(request.remote_addr)).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(1))
		climate_log = ClimateLogModel(
			co2=args['co2'], humidity=args['humidity'], temperature=args['temperature'], IP=ips)
		db.session.add(climate_log)
		db.session.commit()
		return 'SUCCESS', 200


relay_parser = reqparse.RequestParser()
relay_parser.add_argument('ip', type=str, help='Invalid IP')
relay_parser.add_argument('state', type=str, help='Invalid State')
class RelayControl(Resource):
	def get(self):
		args = relay_parser.parse_args()
		ips = IPModel.query.filter_by(ip=args["ip"]).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(1))

		if args["state"] == 'low':
			start_task('low', args["ip"])
		if args["state"] == 'high':
			end_task('high', args["ip"])
		return 'SUCCESS', 200


api.add_resource(APJobInfo, '/ap_jobs')

api.add_resource(Room, '/room/<int:room_id>')
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
	app.run(host='0.0.0.0', debug=False)