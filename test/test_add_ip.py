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
            'IP': '192.168.0.18',
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
count = 3
for p in payload:
	url = f"http://127.0.0.1:5000/room/1/ip/{count}"
	# url = f"/ip"

	response = requests.patch(url)
	print(response.json())
	count+=1
