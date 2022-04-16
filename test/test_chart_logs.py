import requests

url = "http://127.0.0.1:5000/room/1/ip_chart_logs"
payload = {
    "datetimes": "2022/04/04 01:00 PM - 2022/04/04 05:00 PM",
	},

for p in payload:
	response = requests.get(url, params=p)
	print(response.json())
