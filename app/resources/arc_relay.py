from flask_restful import Resource, reqparse, abort
from app import IPModel
from common.util import start_task, end_task

relay_parser = reqparse.RequestParser()
relay_parser.add_argument('ip', type=str, help='Invalid IP')
relay_parser.add_argument('state', type=str, help='Invalid State')


class RelayControl(Resource):
	def get(self):
		args = relay_parser.parse_args()
		ips = db.IPModel.query.filter_by(ip=args["ip"]).first()
		if not ips:
			abort(409, message="IP {} does not exist".format(1))

		if args["state"] == 'low':
			start_task('low', args["ip"])
		if args["state"] == 'high':
			end_task('high', args["ip"])
		return 'SUCCESS', 200
