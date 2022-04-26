import requests

# url = "http://127.0.0.1:5000/ip/1"
# url = "http://192.168.0.215:5000/room/1"
payload = [
	{
	'name': 'Light',
	'IP': '192.168.0.133',
},
	{
	'name': 'Water',
	'IP': '192.168.0.13',
},
	{
	'name': 'Climate',
	'IP': '192.168.0.16',
},
	{
	'name': 'Climate',
	'IP': '192.168.0.23',
},
	{
	'name': 'CO2',
	'IP': '192.168.0.17',
},
	{
	'name': 'Humidity',
	'IP': '192.168.0.14',
},
	{
	'name': 'Temperature',
	'IP': '192.168.0.15',
},
]
count=1
for p in payload:
	url = f"http://127.0.0.1:5000/ip"
	# url = f"http://192.168.1.42:5000/ip"

	response = requests.get(url,params=p)
	print(response.json())
