from datetime import datetime
from flask import request
import json
from app.app import db, api
from app.models import IPModel, ClimateLiveDataModel, ClimateModel, ClimateDayNightModel, ClimateLogModel
from flask_restful import Resource, reqparse, abort, fields, marshal_with
import logging
from .utils import start_task, end_task, get_local_datetime, is_time_between
import math


climate_parser = reqparse.RequestParser()
climate_parser.add_argument('co2', type=int, help='Invalid CO2')
climate_parser.add_argument('humidity', type=float, help='Invalid Humidity')
climate_parser.add_argument('temperature', type=float, help='Invalid Temperature')

class Climate(Resource):
	def get(self):
		args = climate_parser.parse_args()
		# ips = IPModel.query.filter_by(ip='192.168.0.23').first()
		print(request.remote_addr)
		ips = IPModel.query.filter_by(ip=str(request.remote_addr)).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(request.remote_addr))
		vpd = ((6.1078*math.exp(17.08085*args['temperature']/(234.175+args['temperature'])))-(6.1078 *
			math.exp(17.08085*args['temperature']/(234.175+args['temperature']))*(args['humidity']/100)))/10.
		vpd=round(vpd,2)
		fahrenheit = (args['temperature'] * 9/5) + 32
		update_climate_reads = ClimateLiveDataModel.query.filter_by(IP=ips).first()
		if update_climate_reads:
			update_climate_reads.co2 = args['co2']
			update_climate_reads.humidity = args['humidity']
			update_climate_reads.temperature = fahrenheit
			update_climate_reads.vpd = vpd

			db.session.add(update_climate_reads)
			db.session.commit()
		else:
			climate_reads = ClimateLiveDataModel(
				co2=args['co2'], humidity=args['humidity'], temperature=fahrenheit,vpd=vpd,IP=ips)
			db.session.add(climate_reads)
			db.session.commit()
		climate = ClimateModel.query.filter_by(IP=ips).all()
		if not climate:
			abort(409, message="Climate {} does not exist".format(1))
		for c in climate:
			climate_day_night = ClimateDayNightModel.query.filter_by(climate=c).first()
			if climate_day_night:
				if climate_day_night.climate_start_time != climate_day_night.climate_end_time:
					check_time = is_time_between(
						climate_day_night.climate_start_time, climate_day_night.climate_end_time)
					if check_time:
						climate = c
					else:
						climate = ClimateModel.query.filter_by(IP=ips).first()
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
			pass

		try:
			if climate.exhaust_relay_ip == 'False':
				print('do nothing')
			else:
				if fahrenheit >= temperature_buffer:
					start_task('low', climate.exhaust_relay_ip)
				elif fahrenheit <= temperature_buffer and args['humidity'] >= humidity_plus:
					start_task('low', climate.exhaust_relay_ip)
				elif fahrenheit <= temperature_buffer:
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

		return json.dumps(args), 201


class ClimateLog(Resource):
	def get(self):
		args = climate_parser.parse_args()
		# ips = IPModel.query.filter_by(ip='192.168.0.23').first()
		print(request.remote_addr)
		ips = IPModel.query.filter_by(ip=str(request.remote_addr)).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(1))
		log_timestamp = get_local_datetime()
		vpd = ((6.1078*math.exp(17.08085*args['temperature']/(234.175+args['temperature'])))-(6.1078 *
			math.exp(17.08085*args['temperature']/(234.175+args['temperature']))*(args['humidity']/100)))/10.
		vpd = round(vpd, 2)
		fahrenheit = (args['temperature'] * 9/5) + 32
		climate_log = ClimateLogModel(
			co2=args['co2'], humidity=args['humidity'], temperature=fahrenheit, vpd=vpd, timestamp=log_timestamp, IP=ips)
		db.session.add(climate_log)
		db.session.commit()
		return 'SUCCESS', 200



climate_data_reads_marshaller = {
	'id': fields.Integer,
	'co2': fields.String,
	'humidity': fields.String,
	'temperature': fields.Integer,
	'vpd': fields.Float,
}

class ClimateReads(Resource):
	@marshal_with(climate_data_reads_marshaller)
	def get(self,ip):
		climate_reads = ClimateLiveDataModel.query.filter_by(ip_id=ip).first()
		if not climate_reads:
			abort(409, message="Climate Reads IP {} does not exist".format(1))

		return climate_reads, 200


api.add_resource(Climate, '/climate')
api.add_resource(ClimateLog, '/climate/log')
api.add_resource(ClimateReads, '/climate/reads/<int:ip>')
