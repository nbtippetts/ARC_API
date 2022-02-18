import requests
from datetime import datetime,timedelta
starting = datetime.now()
start_min = 1
minutes = 5
start_added = timedelta(minutes = start_min)
end_added = timedelta(minutes = minutes)
start = starting + start_added
end = starting + end_added
print(start)
print(end)
url = "http://127.0.0.1:5000/room/1/relayschedule"
# url = "http://127.0.0.1:5000/room/1/ip/1/relayschedule/1"
# payload={'name': 'light','start_time': start, 'end_time': end, 'how_often': '*'}
# response = requests.put(url, data=payload)
# print(response.json())

# response = requests.get(url)
# print(response.json())

# response = requests.patch(url, data=payload,)
# print(response.text)

response = requests.get(url)
print(response.json())

# response = requests.delete(url)
# print(response)
