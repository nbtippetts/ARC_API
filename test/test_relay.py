import requests

url = f"http://192.168.1.42:5000/relay_control"
payload = {
	'ip': '192.168.1.26',
	'state': 'high'
}
res = requests.get(url,params=payload)
print(res)
print(res.json())
