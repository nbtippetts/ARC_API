from flask_restful import Resource, reqparse, abort, fields, marshal_with, request
from app.services import appscheduler
from app.models import RoomModel, IPModel, ClimateScheduleModel, ClimateModel, ClimateIntervalModel, ClimateDayNightModel, ClimateLogModel, db
from common.util import check_ip_state, start_task, end_task, is_time_between
from websocket import create_connection
import json

climate_day_night_marshaller = {
	'id': fields.Integer,
	'climate_start_time': fields.String,
	'climate_end_time': fields.String,
	'climate_id': fields.Integer,
}

resource_fields = {
	'climate_id': fields.Integer,
	'room_id': fields.Integer,
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
climate_ips_resource_fields = {
	'id': fields.Integer,
	'ip': fields.String,
	'name': fields.String,
}

climate_parameters_parser = reqparse.RequestParser()
climate_parameters_parser.add_argument(
	'name', type=str, help='Invalid Room', required=True)
climate_parameters_parser.add_argument(
	'buffer_parameters', type=int, help='Invalid Buffer INT', required=True)
climate_parameters_parser.add_argument(
	'co2_buffer_parameters', type=int, help='Invalid Buffer INT', required=True)
climate_parameters_parser.add_argument(
	'co2_parameters', type=int, help='Invalid CO2 Data', required=True)
climate_parameters_parser.add_argument(
	'humidity_parameters', type=int, help='Invalid Humidity Data', required=True)
climate_parameters_parser.add_argument(
	'temperature_parameters', type=int, help='Invalid Temperature Data', required=True)
climate_parameters_parser.add_argument(
	'climate_start_time', type=str, help='Invalid climate start date', required=False)
climate_parameters_parser.add_argument(
	'climate_end_time', type=str, help='Invalid climate end date', required=False)
climate_parameters_parser.add_argument(
	'co2_relay_ip', type=str, help='Invalid CO2 IP', required=True)
climate_parameters_parser.add_argument(
	'humidity_relay_ip', type=str, help='Invalid Humidity IP', required=True)
climate_parameters_parser.add_argument(
	'exhaust_relay_ip', type=str, help='Invalid Temperature IP', required=True)


class ClimateParametersIPList(Resource):
	@marshal_with(climate_ips_resource_fields)
	def get(self, room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		check_ips = IPModel.query.filter_by(room=rooms).all()
		valid_ips = []
		ips_names = ['Exhaust', 'Humidity', 'CO2']
		for ips in check_ips:
			if ips.name in ips_names:
				valid_ips.append(ips)
		return valid_ips, 200


class ClimateParametersList(Resource):
	@marshal_with(resource_fields)
	def get(self, room_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		climate = ClimateModel.query.filter_by(room=rooms).all()
		return climate, 200


class ClimateParameters(Resource):
	@marshal_with(resource_fields)
	def get(self, room_id, climate_parameter_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		results = ClimateModel.query.filter_by(
			climate_id=climate_parameter_id, room=rooms).first()
		return results, 200

	@marshal_with(resource_fields)
	def put(self, room_id, climate_parameter_id):
		args = climate_parameters_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		ips = IPModel.query.filter_by(name='Climate', room=rooms).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(ips))
		results = ClimateModel.query.filter_by(
			climate_id=climate_parameter_id, room=rooms).first()
		if results:
			abort(409, message="Climate {} already exist".format(climate_parameter_id))

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

				appscheduler.remove_job(
					f'{interval_id.climate_interval_id}-interval-start')
				appscheduler.remove_job(f'{interval_id.climate_interval_id}-interval-end')
				db.session.delete(interval_id)
				db.session.commit()
				if ips.state:
					check_ip_state(ips)
		check_schedule = ClimateScheduleModel.query.filter(
			ClimateScheduleModel.name.in_(['Exhaust', 'Humidity', 'CO2'])).all()
		if check_schedule:
			for schedule_id in check_schedule:
				start_job = appscheduler.get_job(
					f'{schedule_id.climate_schedule_id}-start')
				if not start_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
						schedule_id.climate_schedule_id))

				end_job = appscheduler.get_job(f'{schedule_id.climate_schedule_id}-end')
				if not end_job:
					abort(409, message="APSchedule Job {} doesn't exist, cannot Delete.".format(
						schedule_id.climate_schedule_id))

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
		if args['climate_start_time'] != '':
			climate_day_night = ClimateDayNightModel(
				climate_start_time=args['climate_start_time'],
				climate_end_time=args['climate_end_time'],
				climate=climate
			)
			db.session.add(climate_day_night)
			db.session.commit()
		return results, 201

	@marshal_with(resource_fields)
	def patch(self, room_id, climate_parameter_id):
		args = climate_parameters_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		climate = ClimateModel.query.filter_by(
			climate_id=climate_parameter_id, room=rooms).first()
		if not climate:
			abort(409, message="Climate Parameters {} doesn't exist, cannot update.".format(
				climate_parameter_id))

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

				appscheduler.remove_job(
					f'{interval_id.climate_interval_id}-interval-start')
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
		climate_day_night = ClimateDayNightModel.query.filter_by(
			climate=climate).first()
		if climate_day_night:
			climate_day_night.climate_start_time = args['climate_start_time'],
			climate_day_night.climate_end_time = args['climate_end_time'],
			db.session.add(climate_day_night)
			db.session.commit()

		return climate, 204

	def delete(self, room_id, climate_parameter_id):
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		climate = ClimateModel.query.filter_by(
			climate_id=climate_parameter_id, room=rooms).first()
		if not climate:
			abort(409, message="climate {} doesn't exist, cannot Delete.".format(
				climate_parameter_id))
		db.session.delete(climate)
		db.session.commit()
		return 'SUCCESS', 204


climate_parser = reqparse.RequestParser()
climate_parser.add_argument('co2', type=int, help='Invalid CO2')
climate_parser.add_argument('humidity', type=float, help='Invalid Humidity')
climate_parser.add_argument(
	'temperature', type=float, help='Invalid Temperature')


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
			# ws = create_connection(f"ws://192.168.1.32:8000/ws/socket-server/")
			ws = create_connection(f"ws://192.168.1.37:8000/ws/socket-server/")
			ws.send(json.dumps({"data": args, "room_id": str(ips.room_id)}))
			result = ws.recv()
			print("Received '%s'" % result)
			ws.close()
		except Exception as e:
			print(e)
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
			if climate.co2_relay_ip == 'False':
				print('do nothing')
			else:
				if args['co2'] <= co2_buffer:
					start_task('low', climate.co2_relay_ip)
				elif args['co2'] >= co2_buffer:
					end_task('high', climate.co2_relay_ip)
				else:
					print('co2 do nothing')
		except Exception as e:
			print(e)
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
			print(e)
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
			print(e)
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
