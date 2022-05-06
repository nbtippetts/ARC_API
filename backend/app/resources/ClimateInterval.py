from app.app import db, appscheduler, api
from app.models import RoomModel, IPModel, ClimateScheduleModel, ClimateIntervalModel, ClimateModel
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from apscheduler.triggers.interval import IntervalTrigger
import logging
from .utils import start_task, end_task, check_ip_state, test_start_task, test_end_task

ip_marshaller = {
	'id': fields.Integer,
	"name": fields.String,
	"state": fields.Boolean,
	"ip": fields.String
}
resource_fields = {
	'climate_interval_id': fields.Integer,
	'room_id': fields.Integer,
	'name': fields.String,
	'interval_hour': fields.Integer,
	'interval_minute': fields.Integer,
	'duration_hour': fields.Integer,
	'duration_minute': fields.Integer,
	"IP": fields.List(fields.Nested(ip_marshaller))
}
# Define parser and request args
interval_parser = reqparse.RequestParser()
interval_parser.add_argument(
	'name', type=str, help='What are you trying to create a schedule for?', required=False)
interval_parser.add_argument(
	'interval_hour', type=int, help='Invalid Interval Hour', required=False)
interval_parser.add_argument(
	'interval_minute', type=int, help='Invalid Interval Minute', required=False)
interval_parser.add_argument(
	'duration_hour', type=int, help='Invalid Duration Hour', required=False)
interval_parser.add_argument(
	'duration_minute', type=int, help='Invalid Duration Minute', required=False)
interval_parser.add_argument(
	'ip_id', type=str, help='Invalid IP', required=False)


class RelayIntervalList(Resource):
	@marshal_with(resource_fields)
	def get(self):
		results = ClimateIntervalModel.query.all()
		return results, 200


class RoomRelayIntervalList(Resource):
	@marshal_with(resource_fields)
	def get(self, room_id):
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
	def get(self, room_id, interval_id):
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			print(job.trigger)
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateIntervalModel.query.filter_by(
			climate_interval_id=interval_id, room=rooms).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self, room_id, interval_id):
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

		interval = ClimateIntervalModel(name=args['name'], interval_hour=args['interval_hour'],
			interval_minute=args['interval_minute'], duration_hour=args['duration_hour'], duration_minute=args['duration_minute'], IP=ip_id, room=rooms)
		db.session.add(interval)
		db.session.commit()

		start_triggers = IntervalTrigger(hours=args['interval_hour'], minutes=args['interval_minute'], jitter=1)
		end_triggers = IntervalTrigger(hours=args['duration_hour'], minutes=args['duration_minute'])
		appscheduler.add_job(start_task, start_triggers, id=f'{interval.climate_interval_id}-interval-start', args=['low', interval.IP.ip], replace_existing=True)
		appscheduler.add_job(end_task, end_triggers, id=f'{interval.climate_interval_id}-interval-end', args=['high', interval.IP.ip], replace_existing=True)
		return interval, 201

	@marshal_with(resource_fields)
	def patch(self, room_id, interval_id):
		args = interval_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		interval = ClimateIntervalModel.query.filter_by(
			climate_interval_id=interval_id, room=rooms).first()
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

		start_triggers = IntervalTrigger(hours=args['interval_hour'], minutes=args['interval_minute'], jitter=1)
		end_triggers = IntervalTrigger(hours=args['duration_hour'], minutes=args['duration_minute'])
		appscheduler.add_job(start_task, start_triggers, id=f'{interval_id}-interval-start', args=['low', interval.IP.ip], replace_existing=True)
		appscheduler.add_job(end_task, end_triggers, id=f'{interval_id}-interval-end', args=['high', interval.IP.ip], replace_existing=True)
		return interval, 201

	def delete(self, room_id, interval_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		interval = ClimateIntervalModel.query.filter_by(
			climate_interval_id=interval_id, room=rooms).first()
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


api.add_resource(
	RelayInterval, '/room/<int:room_id>/relayinterval/<int:interval_id>')
api.add_resource(RoomRelayIntervalList, '/room/<int:room_id>/relayinterval')
api.add_resource(RelayIntervalList, '/relayinterval')
