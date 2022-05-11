import requests

url = f"http://localhost:5000/relay_control"
payload = {
	'ip': '192.168.0.133',
	'state': 'low'
}

res = requests.get(url,params=payload)
print(res)
print(res.json())
