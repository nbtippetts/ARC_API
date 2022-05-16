import requests

# url = "http://127.0.0.1:5000/ip/1"
# url = "http://192.168.0.215:5000/room/1"
payload = {
	'ssid': 'Hidden_Wifi_Village',
	'password': 'largecartoon258',
}

# url = f"http://127.0.0.1:5000/wifi"
url = "http://192.168.1.42:5000/wifi"

response = requests.get(url, params=payload)
print(response.json())
