import logging
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from app.models import RoomModel, IPModel
from app.app import db, api

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
	'vpd': fields.Float,
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

		climate_schedule_log = [p.climate_schedule_log for p in IPModel.query.filter_by(
			room=rooms).limit(100).all() if p.climate_schedule_log]
		all_schedule_logs = []
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

		climate_log = [p.climate_log for p in IPModel.query.filter_by(
			room=rooms).limit(100).all() if p.climate_log]
		if len(climate_log) > 0:
			for log in climate_log[0]:
				log.timestamp = log.timestamp.strftime('%d %b, %I:%M %p')
			return {'climate_log': climate_log}, 200
		else:
			return {'climate_log': climate_log}, 204


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


api.add_resource(AddIP, '/ip')
api.add_resource(IPLogs, '/room/<int:room_id>/ip_logs')
api.add_resource(IPChartLogs, '/room/<int:room_id>/ip_chart_logs')
api.add_resource(IPList, '/all_ips')
