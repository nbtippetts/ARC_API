import requests

# url = "http://127.0.0.1:5000/ip/1"
# url = "http://192.168.0.215:5000/room/1"
payload = [{
	'name': 'Climate',
	'IP': '192.168.0.133',
}, {
	'name': 'CO2',
	'IP': '192.168.0.138',
}, {
	'name': 'Humidity',
	'IP': '192.168.0.131',
}, {
	'name': 'Exhaust',
	'IP': '192.168.0.132',
}]
count=1
for p in payload:
	url = f"http://127.0.0.1:5000/ip"
	# url = f"http://192.168.1.37:5000/ip"

	response = requests.get(url,params=p)
	print(response.json())



# class RoomList(Resource):
# 	@marshal_with(resource_fields)
# 	def get(self):
# 		rooms = RoomModel.query.all()
# 		if not rooms:
# 			abort(409, message="Rooms do not exist")
# 		all_rooms = []
# 		for room in rooms:
# 			rooms_data = {}
# 			climate_schedule = ClimateScheduleModel.query.filter_by(room=room).all()
# 			if not climate_schedule:
# 				rooms_data['climate_schedule'] = []
# 			else:
# 				for room in climate_schedule:
# 				rooms_data['climate_schedule'] = [room.climate_schedule_id,
#                                       room.name, room.start_time, room.end_time, room.how_often, ]

# 			climate = ClimateModel.query.filter_by(room=room).all()
# 			if not climate:
# 				rooms_data['climate'] = []
# 			else:
# 				for room in climate:
# 				rooms_data['climate'] = [room.climate_id, room.name, room.co2_parameters, room.humidity_parameters,
#                                     room.temperature_parameters, room.co2_relay_ip, room.humidity_relay_ip, room.exhaust_relay_ip, ]

# 			ip = IPModel.query.filter_by(room=room).all()
# 			if not ip:
# 				rooms_data['ip'] = []
# 			else:
# 				for room in ip:
# 					rooms_data['ip'] = [room.ip]

# 			notebook = NoteBookModel.query.filter_by(room=room).all()
# 			if not notebook:
# 				rooms_data['notebook'] = []
# 			else:
# 				for room in notebook:
# 				rooms_data['notebook'] = [room.notebook_id,
#                                     room.title, room.body, room.publish_date, ]

# 			all_rooms.append(rooms_data)
# 		return all_rooms, 200
