import yaml
import os
from flask_restful import Resource, reqparse, abort
from app.app import api

wifi_parser = reqparse.RequestParser()
wifi_parser.add_argument(
	'ssid', type=str, help='Invalid ssid', required=True)
wifi_parser.add_argument(
	'password', type=str, help='Invalid password', required=True)


class WifiConf(Resource):
	def get(self):
		args = wifi_parser.parse_args()
		with open('app/resources/wifi.yaml') as file:
			wifi_conf = yaml.load(file, Loader=yaml.FullLoader)
		wifi_conf['network']['wifis']['wlan0']['access-points'][args['ssid']] = wifi_conf['network']['wifis']['wlan0']['access-points'].pop('SSID')
		wifi_conf['network']['wifis']['wlan0']['access-points'][args['ssid']]['password'] = args['password']
		print(wifi_conf)
		with open('/etc/netplan/50-cloud-init.yaml', 'w') as file:
			documents = yaml.dump(wifi_conf, file)
		try:
			gen = os.system("netplan generate")
			apply = os.system("netplan apply")
		except Exception as e:
			print(e)
			abort(409)
		return "Freak Ya", 200


api.add_resource(WifiConf, '/wifi')
