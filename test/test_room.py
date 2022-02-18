import requests

url = "http://127.0.0.1:5000/room/1"
# url = "http://192.168.0.215:5000/room/1"
payload={
	'name': 'room1',
}
response = requests.put(url, data=payload)
print(response.json())

response = requests.get(url)
print(response.json())

response = requests.patch(url, data=payload,)
print(response.text)

response = requests.get(url)
print(response.json())

# response = requests.delete(url)
# print(response)
