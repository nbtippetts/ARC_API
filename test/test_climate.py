import requests

# url = "http://127.0.0.1:5000/room/1/climate-parameters/1"
# # url = "http://192.168.0.215:5000/room/1/climate-parameters/1"
# payload={
# 	'name': 'Room ONE',
# 	'co2_parameters': 500,
# 	'humidity_parameters': 20,
# 	'temperature_parameters': 80,
# 	'co2_relay_ip': '192.168.0.138',
# 	'humidity_relay_ip': '192.168.0.666',
# 	'exhaust_relay_ip': '192.168.0.69'
# }
url = "http://127.0.0.1:5000/climate"
# url = "http://192.168.0.215:5000/room/1/climate-parameters/1"
payload={
    "co2": 500,
    "humidity": 20,
    "temperature": 80
}
# response = requests.put(url, data=payload)
# print(response.json())

response = requests.get(url, params=payload)
print(response.json())

# response = requests.patch(url, data=payload,)
# print(response.text)

# response = requests.get(url)
# print(response.json())

# response = requests.delete(url)
# print(response)
