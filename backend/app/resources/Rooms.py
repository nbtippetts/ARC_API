import logging
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import RoomModel, IPModel, ClimateLogModel
from app.app import db, appscheduler, api
from flask import make_response
from datetime import datetime

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
	'timestamp': fields.String,
	'ip_id': fields.Integer,
}
climate_log_marshaller = {
	'climate_log_id': fields.Integer,
	'co2': fields.Integer,
	'humidity': fields.Integer,
	'temperature': fields.Integer,
	'timestamp': fields.String,
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
chart_logs_resource_fields = {
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
ip_parser.add_argument(
	'IP', type=str, help='Invalid IP Address', required=True)


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

		climate_schedule_log = [p.climate_schedule_log[:50] for p in IPModel.query.filter_by(room=rooms).all() if p.climate_schedule_log]
		all_schedule_logs=[]
		if len(climate_schedule_log) > 0:
			for log in climate_schedule_log:
				for ft in log:
					ft.timestamp = ft.timestamp.strftime('%d %b')
					all_schedule_logs.append(ft)
			return {'climate_schedule_log': all_schedule_logs}, 200
		else:
			return {'climate_schedule_log': climate_schedule_log}, 204


log_chart_parser = reqparse.RequestParser()
log_chart_parser.add_argument(
	'datetimes', type=str, help='Invalid Datetimes', required=False)


class IPChartLogs(Resource):
	@marshal_with(logs_resource_fields)
	def get(self, room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))

		climate_log = [p.climate_log[:100]for p in IPModel.query.filter_by(room=rooms).all() if p.climate_log]
		if len(climate_log) > 0:
			for log in climate_log[0]:
				log.timestamp = log.timestamp.strftime('%d %b, %I:%M %p')
			return {'climate_log': climate_log}, 200
		else:
			return {'climate_log': climate_log}, 204


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
		# args = ip_parser.parse_args()
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
		ap_job_list = []
		jobs = appscheduler.get_jobs()
		print(jobs)
		for job in jobs:
			ap_job_list.append((job.id, job.trigger))

		return make_response(str(ap_job_list), 200)


api.add_resource(APJobInfo, '/ap_jobs')

api.add_resource(Room, '/room/<int:room_id>')
api.add_resource(RoomList, '/rooms')

api.add_resource(AddIP, '/ip')
api.add_resource(RoomIP, '/room/<int:room_id>/ip/<int:ip_id>')
api.add_resource(IPLogs, '/room/<int:room_id>/ip_logs')
api.add_resource(IPChartLogs, '/room/<int:room_id>/ip_chart_logs')
api.add_resource(IPList, '/all_ips')
