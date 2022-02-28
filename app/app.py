from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import utc
import requests
import json
import urllib.parse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from sqlalchemy import null
from websocket import create_connection
import os


app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ARC.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:{}@localhost/arc_db".format(
# 	urllib.parse.quote_plus("@Wicked2009"))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
	os.getenv('DB_USER', 'flask'),
	os.getenv('DB_PASSWORD', ''),
	os.getenv('DB_HOST', 'mysql'),
	os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)

jobstores = {
	# 'default': SQLAlchemyJobStore(url="mysql+pymysql://root:{}@localhost/arc_db".format( urllib.parse.quote_plus("@Wicked2009")))
	'default': SQLAlchemyJobStore(url='mysql+pymysql://{}:{}@{}/{}'.format(
		os.getenv('DB_USER', 'flask'),
		os.getenv('DB_PASSWORD', ''),
		os.getenv('DB_HOST', 'mysql'),
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
appscheduler = BackgroundScheduler(daemon=True, jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)
appscheduler.start()
# appscheduler.shutdown()

class RoomModel(db.Model):
	__tablename__ = 'room'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	climate_schedule = db.relationship('ClimateScheduleModel', backref='room',lazy='joined')
	climate_schedule_log = db.relationship('ClimateScheduleLogModel', backref='room',lazy='joined')
	climate = db.relationship('ClimateModel', backref='room',lazy='joined')
	climate_log = db.relationship('ClimateLogModel', backref='room',lazy='joined')
	notebook = db.relationship('NoteBookModel', backref='room', lazy='joined')
	ip = db.relationship('IPModel', backref='room', lazy='joined')
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)

class IPModel(db.Model):
	__tablename__ = 'IP'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	ip = db.Column(db.String(20), nullable=False)
	climate_schedule = db.relationship('ClimateScheduleModel', backref='IP', lazy='joined')
	climate = db.relationship('ClimateModel', backref='IP', lazy='joined')
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)
class ClimateScheduleModel(db.Model):
	__tablename__ = 'climate_schedule'
	climate_schedule_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.DateTime, nullable=False)
	end_time = db.Column(db.DateTime, nullable=False)
	how_often = db.Column(db.String(20), nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)
class ClimateScheduleLogModel(db.Model):
	__tablename__ = 'climate_schedule_log'
	climate_schedule_log_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.DateTime, nullable=False)
	end_time = db.Column(db.DateTime, nullable=False)
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)

class ClimateModel(db.Model):
	__tablename__ = 'climate'
	climate_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	co2_parameters = db.Column(db.Integer, nullable=False)
	humidity_parameters = db.Column(db.Integer, nullable=False)
	temperature_parameters = db.Column(db.Integer, nullable=False)
	co2_relay_ip = db.Column(db.String(20), nullable=False)
	humidity_relay_ip = db.Column(db.String(20), nullable=False)
	exhaust_relay_ip = db.Column(db.String(20), nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)

class ClimateLogModel(db.Model):
	__tablename__ = 'climate_log'
	climate_log_id = db.Column(db.Integer, primary_key=True)
	co2 = db.Column(db.Integer, nullable=False)
	humidity = db.Column(db.Integer, nullable=False)
	temperature = db.Column(db.Integer, nullable=False)
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)


class NoteBookModel(db.Model):
	__tablename__ = 'notebook'
	notebook_id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	body = db.Column(db.String(800), nullable=False)
	publish_date = db.Column(db.DateTime, nullable=False)
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
	)


@app.before_first_request
def create_tables():
	db.create_all()

def start_task(*args):
	print(args)
	url = f'http://{args[1]}/io?v={args[0]}'
	res = requests.get(url)
	print(res.status_code)
	print(args)
	# print(url)
	return args
def end_task(*args):
	url = f'http://{args[1]}/io?v={args[0]}'
	res = requests.get(url)
	print(res.status_code)
	print(args)
	return args


ip_marshaller = {
	'id': fields.Integer,
	"name": fields.String,
	"ip": fields.String
}
climate_schedule_marshaller = {
	'climate_schedule_id': fields.Integer,
	'name': fields.String,
	'start_time': fields.DateTime,
	'end_time': fields.DateTime,
	"IP": fields.List(fields.Nested(ip_marshaller))
}

climate_marshaller = {
	'climate_id': fields.Integer,
	'name': fields.String,
	'co2_parameters': fields.Integer,
	'humidity_parameters': fields.Integer,
	'temperature_parameters': fields.Integer,
	'co2_relay_ip': fields.String,
	'humidity_relay_ip': fields.String,
	'exhaust_relay_ip': fields.String,
}

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'climate_schedule': fields.Nested(climate_schedule_marshaller),
	'climate_schedule_log': fields.Nested(climate_schedule_marshaller),
	'climate': fields.Nested(climate_marshaller),
	'climate_log': fields.Nested(climate_schedule_marshaller),
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
		print(results.climate_schedule)
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


resource_fields = {
	'id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'ip': fields.String,
	'climate_schedule': fields.String,
	'climate': fields.String,
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

class IPRoomList(Resource):
	@marshal_with(resource_fields)
	def get(self, room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = IPModel.query.filter_by(room=rooms).all()
		return results, 200


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


resource_fields = {
	'climate_schedule_id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'start_time': fields.DateTime,
	'end_time': fields.DateTime,
	'ip_id': fields.Integer,
}
# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='What are you trying to create a schedule for?', required=True)
parser.add_argument('start_time', type=str, help='Invalid Date', required=True)
parser.add_argument('end_time', type=str, help='Invalid Date', required=True)
parser.add_argument('how_often', type=str, help='Invalid Interval', required=True)
parser.add_argument('ip_id', type=int, help='Invalid IP', required=True)


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
		# ip_id.name = args['name']
		db.session.add(ip_id)
		db.session.commit()
		results = ClimateScheduleModel.query.filter_by(climate_schedule_id=schedule_id, IP=ip_id,room=rooms).first()
		if results:
			abort(409, message="Schedule {} already exist".format(schedule_id))
		schedule = ClimateScheduleModel(climate_schedule_id=schedule_id, name=args['name'], start_time=args['start_time'], end_time=args['end_time'], how_often=args['how_often'], IP=ip_id,room=rooms)
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")
		appscheduler.add_job(id=f'{schedule_id}-start', func=start_task, trigger='cron',second=5, args=['low',schedule.IP.ip],replace_existing=True)
		appscheduler.add_job(id=f'{schedule_id}-end', func=end_task, trigger='cron',second=30, args=['high',schedule.IP.ip], replace_existing=True)
		# appscheduler.add_job(id=f'{schedule_id}-start', func=start_task, trigger='cron', day_of_week=args['how_often'],hour=start_hour, minute=start_minute, args=['low', schedule.IP.ip], replace_existing=True)
		# appscheduler.add_job(id=f'{schedule_id}-end', func=end_task, trigger='cron', day_of_week=args['how_often'], hour=end_hour, minute=end_minute, args=['high', schedule.IP.ip], replace_existing=True)
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
		schedule.start_time = args['start_time']
		schedule.end_time = args['end_time']
		schedule.how_often = args['how_often']
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		# appscheduler.add_job(id=f'{schedule_id}-start', func=start_task, trigger='cron',second=5, args=['low',ip.ip],replace_existing=True)
		# appscheduler.add_job(id=f'{schedule_id}-end', func=end_task, trigger='cron',second=30, args=['high',ip.ip], replace_existing=True)
		appscheduler.add_job(id=f'{schedule_id}-start', func=start_task, trigger='cron',
							 day_of_week=args['how_often'], hour=start_hour, minute=start_minute, args=['low', schedule.IP.ip], replace_existing=True)
		appscheduler.add_job(id=f'{schedule_id}-end', func=end_task, trigger='cron',
							 day_of_week=args['how_often'], hour=end_hour, minute=end_minute, args=['high', schedule.IP.ip], replace_existing=True)

		return 'Successfuly Updated', 204

	def delete(self,room_id,schedule_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		schedule = ClimateScheduleModel.query.filter_by(climate_schedule_id=schedule_id, room=rooms).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot Delete.".format(schedule_id))
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
	'climate_id': fields.Integer,
	'room_id': fields.Integer,
	'name':fields.String,
	'co2_parameters':fields.Integer,
	'humidity_parameters':fields.Integer,
	'temperature_parameters':fields.Integer,
	'co2_relay_ip':fields.String,
	'humidity_relay_ip':fields.String,
	'exhaust_relay_ip':fields.String,
}
climate_ips_resource_fields = {
	'id': fields.Integer,
	'ip': fields.String,
	'name':fields.String,
}

climate_parameters_parser = reqparse.RequestParser()
climate_parameters_parser.add_argument('name', type=str, help='Invalid Room', required=True)
climate_parameters_parser.add_argument('co2_parameters', type=int, help='Invalid CO2 Data', required=True)
climate_parameters_parser.add_argument('humidity_parameters', type=int, help='Invalid Humidity Data', required=True)
climate_parameters_parser.add_argument('temperature_parameters', type=int, help='Invalid Temperature Data', required=True)
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
		# check_ips = db.session.query(IPModel).filter(IPModel.ip.in_((args['co2_relay_ip'], args['humidity_relay_ip'], args['exhaust_relay_ip']))).all()
		# if not check_ips:
		# 	abort(409, message="Relay {} does not exist".format(check_ips))
		# for ips in check_ips:
		# 	ips.name = args['name']
		# 	db.session.add(ips)
		# db.session.commit()
		climate = ClimateModel(climate_id=climate_parameter_id, name=args['name'], co2_parameters=args['co2_parameters'], humidity_parameters=args['humidity_parameters'],
			temperature_parameters=args['temperature_parameters'], co2_relay_ip=args['co2_relay_ip'], humidity_relay_ip=args['humidity_relay_ip'], exhaust_relay_ip=args['exhaust_relay_ip'], IP=ips, room=rooms)
		db.session.add(climate)
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

		# climate.name = args['name']
		climate.co2_parameters = args['co2_parameters']
		climate.humidity_parameters = args['humidity_parameters']
		climate.temperature_parameters = args['temperature_parameters']
		climate.co2_relay_ip = args['co2_relay_ip']
		climate.humidity_relay_ip = args['humidity_relay_ip']
		climate.exhaust_relay_ip = args['exhaust_relay_ip']

		db.session.add(climate)
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

		# ips = IPModel.query.filter_by(ip='192.168.1.12').first()
		ips = IPModel.query.filter_by(ip=request.remote_addr).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(1))
		ws = create_connection(
			f"ws://192.168.1.37:8000/ws/socket-server/")
		# ws = create_connection(
		# 	f"ws://127.0.0.1:8000/ws/socket-server/")
		ws.send(json.dumps({"data": args, "room_id": str(ips.room_id)}))
		result = ws.recv()
		print("Received '%s'" % result)
		ws.close()
		# climate_log = ClimateLogModel(co2=args['co2'], humidity=args['humidity'], temperature=args['temperature'], room=rooms)
		# db.session.add(climate_log)
		# db.session.commit()
		# climate = ClimateModel.query.filter_by(IP=ips).first()
		# if not climate:
		# 	abort(409, message="Climate {} does not exist".format(1))

		# try:
		# 	if args['co2'] <= climate.co2_parameters:
		# 		co2_url = f'http://{climate.co2_relay_ip}/io?v=low'
		# 		# start_task('low', climate.co2_relay_ip)
		# 		print(co2_url)
		# 		co2_res = requests.get(co2_url)
		# 		print(co2_res.status_code)
		# 	elif args['co2'] >= climate.co2_parameters:
		# 		co2_url = f'http://{climate.co2_relay_ip}/io?v=high'
		# 		print(co2_url)
		# 		co2_res = requests.get(co2_url)
		# 		print(co2_res.status_code)
		# 		# end_task('high', climate.co2_relay_ip)
		# 	else:
		# 		print('co2 do nothing')
		# except Exception as e:
		# 	print(e)
		# 	pass

		# try:
		# 	if args['temperature'] >= climate.temperature_parameters:
		# 		exhaust_url = f'http://{climate.exhaust_relay_ip}/io?v=low'
		# 		print(exhaust_url)
		# 		exhaust_res = requests.get(exhaust_url)
		# 		print(exhaust_res.status_code)
		# 		# start_task('low', climate.exhaust_relay_ip)
		# 	elif args['temperature'] <= climate.temperature_parameters and args['humidity'] >= climate.humidity_parameters:
		# 		exhaust_url = f'http://{climate.exhaust_relay_ip}/io?v=low'
		# 		print(exhaust_url)
		# 		exhaust_res = requests.get(exhaust_url)
		# 		print(exhaust_res.status_code)
		# 	elif args['temperature'] <= climate.temperature_parameters:
		# 		exhaust_url = f'http://{climate.exhaust_relay_ip}/io?v=high'
		# 		print(exhaust_url)
		# 		exhaust_res = requests.get(exhaust_url)
		# 		print(exhaust_res.status_code)
		# 		# end_task('high', climate.exhaust_relay_ip)
		# 	else:
		# 		print('temp do nothing')
		# except Exception as e:
		# 	print(e)
		# 	pass
		# try:
		# 	if args['humidity'] <= climate.humidity_parameters:
		# 		humidity_url = f'http://{climate.humidity_relay_ip}/io?v=low'
		# 		print(humidity_url)
		# 		humidity_res = requests.get(humidity_url)
		# 		print(humidity_res.status_code)
		# 		# start_task('low', climate.humidity_relay_ip)
		# 	elif args['humidity'] >= climate.humidity_parameters:
		# 		humidity_url = f'http://{climate.humidity_relay_ip}/io?v=high'
		# 		print(humidity_url)
		# 		humidity_res = requests.get(humidity_url)
		# 		print(humidity_res.status_code)
		# 		# end_task('high', climate.humidity_relay_ip)
		# 	else:
		# 		print('humidity do nothing')

		# except Exception as e:
		# 	print(e)
		# 	pass

		return 'SUCCESS', 200


api.add_resource(Room, '/room/<int:room_id>')
api.add_resource(RoomList, '/rooms')

api.add_resource(AddIP, '/ip')
api.add_resource(RoomIP, '/room/<int:room_id>/ip/<int:ip_id>')
api.add_resource(IPRoomList, '/room/<int:room_id>/ips')
api.add_resource(IPList, '/all_ips')

api.add_resource(RelaySchedule, '/room/<int:room_id>/relayschedule/<int:schedule_id>')
api.add_resource(RoomRelayScheduleList, '/room/<int:room_id>/relayschedule')
api.add_resource(RelayScheduleList, '/relayschedule')

api.add_resource(ClimateParameters,'/room/<int:room_id>/climate/<int:climate_parameter_id>')
api.add_resource(ClimateParametersIPList, '/room/<int:room_id>/climate_ips')
api.add_resource(ClimateParametersList,'/room/<int:room_id>/climate')

api.add_resource(Climate, '/climate')

if __name__ == '__main__':
	app.run(host='0.0.0.0')