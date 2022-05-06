from datetime import datetime
from app.app import db, appscheduler, api
from app.models import RoomModel, IPModel, ClimateScheduleModel, ClimateIntervalModel, ClimateModel
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from apscheduler.triggers.cron import CronTrigger
import logging
from .utils import start_task, end_task, get_local_time, is_time_between, check_ip_state

ip_marshaller = {
	'id': fields.Integer,
	"name": fields.String,
	"state": fields.Boolean,
	"ip": fields.String
}

resource_fields = {
	'climate_schedule_id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'start_time': fields.String,
	'end_time': fields.String,
	"IP": fields.List(fields.Nested(ip_marshaller))
}
# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='What are you trying to create a schedule for?', required=False)
parser.add_argument('start_time', type=str, help='Invalid Date', required=True)
parser.add_argument('end_time', type=str, help='Invalid Date', required=True)
parser.add_argument('how_often', type=str,help='Invalid Interval', required=True)
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
	def get(self, room_id):
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
	def get(self, room_id, schedule_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateScheduleModel.query.filter_by(
			climate_schedule_id=schedule_id, room=rooms).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self, room_id, schedule_id):
		args = parser.parse_args()
		args['start_time'] = datetime.strptime(args['start_time'], '%m/%d/%Y, %I:%M:%S %p')
		args['end_time'] = datetime.strptime(args['end_time'], '%m/%d/%Y, %I:%M:%S %p')
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
				remove_ip.co2_relay_ip = 'False'
				if ip_id.state:
					check_ip_state(ip_id)
			if remove_ip.humidity_relay_ip == ip_id.ip:
				remove_ip.humidity_relay_ip = 'False'
				if ip_id.state:
					check_ip_state(ip_id)
			if remove_ip.exhaust_relay_ip == ip_id.ip:
				remove_ip.exhaust_relay_ip = 'False'
				if ip_id.state:
					check_ip_state(ip_id)

			db.session.add(remove_ip)
			db.session.commit()
		check_interval = ClimateIntervalModel.query.filter_by(IP=ip_id).first()
		if check_interval:
			start_job = appscheduler.get_job(
				f'{check_interval.climate_interval_id}-interval-start')
			if not start_job:
				abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
					check_interval.climate_interval_id))

			end_job = appscheduler.get_job(
				f'{check_interval.climate_interval_id}-interval-end')
			if not end_job:
				abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
					check_interval.climate_interval_id))

			appscheduler.remove_job(
				f'{check_interval.climate_interval_id}-interval-start')
			appscheduler.remove_job(
				f'{check_interval.climate_interval_id}-interval-end')
			db.session.delete(check_interval)
			db.session.commit()
			if ip_id.state:
				check_ip_state(ip_id)

		start_display = args['start_time'].strftime("%I:%M %p")
		end_display = args['end_time'].strftime("%I:%M %p")
		schedule = ClimateScheduleModel(name=args['name'], start_time=start_display, end_time=end_display, how_often=args['how_often'], IP=ip_id, room=rooms)
		try:
			db.session.add(schedule)
			db.session.commit()
		except Exception as e:
			print(e)

		start_hour = args['start_time'].strftime("%H")
		start_minute = args['start_time'].strftime("%M")

		end_hour = args['end_time'].strftime("%H")
		end_minute = args['end_time'].strftime("%M")

		start_triggers = CronTrigger(hour=start_hour, minute=start_minute)
		end_triggers = CronTrigger(hour=end_hour, minute=end_minute)
		appscheduler.add_job(start_task, start_triggers, id=f'{schedule.climate_schedule_id}-start', args=[
                    'low', schedule.IP.ip], replace_existing=True)
		appscheduler.add_job(end_task, end_triggers, id=f'{schedule.climate_schedule_id}-end', args=[
                    'high', schedule.IP.ip], replace_existing=True)
		return schedule, 201

	@marshal_with(resource_fields)
	def patch(self, room_id, schedule_id):
		args = parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		schedule = ClimateScheduleModel.query.filter_by(
			climate_schedule_id=schedule_id, room=rooms).first()
		if not schedule:
			abort(409, message="Schedule {} doesn't exist, cannot update.".format(schedule_id))

		args['start_time'] = datetime.strptime(args['start_time'], '%m/%d/%Y, %I:%M:%S %p')
		args['end_time'] = datetime.strptime(args['end_time'], '%m/%d/%Y, %I:%M:%S %p')
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
		return schedule, 201

	def delete(self, room_id, schedule_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		schedule = ClimateScheduleModel.query.filter_by(
			climate_schedule_id=schedule_id, room=rooms).first()
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


api.add_resource(RelayControl, '/relay_control')
api.add_resource(RelaySchedule, '/room/<int:room_id>/relayschedule/<int:schedule_id>')
api.add_resource(RoomRelayScheduleList, '/room/<int:room_id>/relayschedule')
api.add_resource(RelayScheduleList, '/relayschedule')
