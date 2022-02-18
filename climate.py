from dataclasses import field
from importlib.metadata import requires
import marshal
import resource
from unittest import result
from xmlrpc.client import DateTime
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import utc
import requests
import json

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
	'default': SQLAlchemyJobStore(url='sqlite:///ARC.db')
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

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ARC.db'
db = SQLAlchemy(app)
appscheduler.start()
# appscheduler.shutdown()

class ScheduleModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.DateTime, nullable=False)
	end_time = db.Column(db.DateTime, nullable=False)
	relay_ip = db.Column(db.String(20), nullable=False)

	def __repr__(self):
		return f'Schedule(name = {self.name}, start_time = {self.start_time}, end_time = {self.end_time}, relay_ip = {self.relay_ip})'
db.create_all()
resource_fields = {
	'id': fields.Integer,
	'start_time': fields.DateTime,
	'end_time': fields.DateTime,
	'relay_ip': fields.String,
}
# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='What are you trying to create a schedule for?', required=True)
parser.add_argument('start_time', type=str, help='Invalid Date', required=True)
parser.add_argument('end_time', type=str, help='Invalid Date', required=True)
parser.add_argument('relay_ip', type=str, help='Invalid IP', required=True)

def start_task(*args):
	print(args)
	url = f'http://{args[1]}/RELAY={args[0]}'
	res = requests.get(url)
	print(res.content)
	# print(url)
	return args
def end_task(*args):
	url = f'http://{args[1]}/RELAY={args[0]}'
	res = requests.get(url)
	print(res.content)
	return args

class WaterSchedule(Resource):

	@marshal_with(resource_fields)
	def get(self, water_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		results = ScheduleModel.query.filter_by(id=water_id).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self,water_id):
		args = parser.parse_args()
		args['start_time']=datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S.%f')
		args['end_time']=datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S.%f')
		results = ScheduleModel.query.filter_by(id=water_id).first()
		if results:
			abort(409, message="Schedule {} already exist".format(water_id))
		schedule = ScheduleModel(id=water_id, name=args['name'], start_time=args['start_time'], end_time=args['end_time'], relay_ip=args['relay_ip'])
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		appscheduler.add_job(id=f'{water_id}-start', func=start_task, trigger='cron',hour=start_hour, minute=start_minute, args=['ON',args['relay_ip']])
		appscheduler.add_job(id=f'{water_id}-end', func=end_task, trigger='cron',hour=end_hour, minute=end_minute, args=['OFF',args['relay_ip']])
		return schedule, 201

	@marshal_with(resource_fields)
	def patch(self,water_id):
		args = parser.parse_args()
		schedule = ScheduleModel.query.filter_by(id=water_id).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot update.".format(water_id))

		args['start_time']=datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S.%f')
		args['end_time']=datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S.%f')
		schedule.start_time = args['start_time']
		schedule.end_time = args['end_time']
		schedule.relay_ip = args['relay_ip']
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		appscheduler.add_job(id=f'{water_id}-start', func=start_task, trigger='cron',second=5, args=['ON',args['relay_ip']],replace_existing=True)
		appscheduler.add_job(id=f'{water_id}-end', func=end_task, trigger='cron',second=30, args=['OFF',args['relay_ip']], replace_existing=True)
		# appscheduler.add_job(id=f'{water_id}-start', func=start_task, trigger='cron',hour=start_hour, minute=start_minute, args=['ON',args['relay_ip']], replace_existing=True)
		# appscheduler.add_job(id=f'{water_id}-end', func=end_task, trigger='cron',hour=end_hour, minute=end_minute, args=['OFF',args['relay_ip']], replace_existing=True)
		return schedule, 204

	def delete(self, water_id):
		schedule = ScheduleModel.query.filter_by(id=water_id).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot Delete.".format(water_id))
		db.session.delete(schedule)
		db.session.commit()

		start_job = appscheduler.get_job(f'{water_id}-start')
		if not start_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(water_id))

		end_job = appscheduler.get_job(f'{water_id}-end')
		if not end_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(water_id))

		appscheduler.remove_job(f'{water_id}-start')
		appscheduler.remove_job(f'{water_id}-end')

		return '', 204

class LightingSchedule(Resource):

	@marshal_with(resource_fields)
	def get(self, lighting_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		results = ScheduleModel.query.filter_by(id=lighting_id).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self,lighting_id):
		args = parser.parse_args()
		args['start_time']=datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S.%f')
		args['end_time']=datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S.%f')
		results = ScheduleModel.query.filter_by(id=lighting_id).first()
		if results:
			abort(409, message="Schedule {} already exist".format(lighting_id))
		schedule = ScheduleModel(id=lighting_id, name=args['name'], start_time=args['start_time'], end_time=args['end_time'], relay_ip=args['relay_ip'])
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		appscheduler.add_job(id=f'{lighting_id}-start', func=start_task, trigger='cron',hour=start_hour, minute=start_minute, args=['ON',args['relay_ip']])
		appscheduler.add_job(id=f'{lighting_id}-end', func=end_task, trigger='cron',hour=end_hour, minute=end_minute, args=['OFF',args['relay_ip']])
		return schedule, 201

	@marshal_with(resource_fields)
	def patch(self,lighting_id):
		args = parser.parse_args()
		schedule = ScheduleModel.query.filter_by(id=lighting_id).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot update.".format(lighting_id))

		args['start_time']=datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S.%f')
		args['end_time']=datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S.%f')
		schedule.start_time = args['start_time']
		schedule.end_time = args['end_time']
		schedule.relay_ip = args['relay_ip']
		db.session.add(schedule)
		db.session.commit()

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		appscheduler.add_job(id=f'{lighting_id}-start', func=start_task, trigger='cron',second=5, args=['ON',args['relay_ip']],replace_existing=True)
		appscheduler.add_job(id=f'{lighting_id}-end', func=end_task, trigger='cron',second=30, args=['OFF',args['relay_ip']], replace_existing=True)
		# appscheduler.add_job(id=f'{lighting_id}-start', func=start_task, trigger='cron',hour=start_hour, minute=start_minute, args=['ON',args['relay_ip']], replace_existing=True)
		# appscheduler.add_job(id=f'{lighting_id}-end', func=end_task, trigger='cron',hour=end_hour, minute=end_minute, args=['OFF',args['relay_ip']], replace_existing=True)
		return schedule, 204

	def delete(self, lighting_id):
		schedule = ScheduleModel.query.filter_by(id=lighting_id).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot Delete.".format(lighting_id))
		db.session.delete(schedule)
		db.session.commit()

		start_job = appscheduler.get_job(f'{lighting_id}-start')
		if not start_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(lighting_id))

		end_job = appscheduler.get_job(f'{lighting_id}-end')
		if not end_job:
			abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(lighting_id))

		appscheduler.remove_job(f'{lighting_id}-start')
		appscheduler.remove_job(f'{lighting_id}-end')

		return '', 204

# class Climate(Resource):
# 	def get(self)

api.add_resource(WaterSchedule, '/waterschedule/<int:water_id>')
api.add_resource(LightingSchedule, '/lightingschedule/<int:lighting_id>')

if __name__ == '__main__':
	app.run(host='0.0.0.0')