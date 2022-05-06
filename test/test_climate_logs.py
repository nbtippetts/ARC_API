import requests
from time import sleep
import random

url = "http://localhost:5000/climate/log"
while True:
	co2 = random.randint(500, 2000)
	hum = random.randint(10, 60)
	temp = random.randint(50, 95)
	payload = {
		"co2": co2,
		"humidity": hum,
		"temperature": temp
	}
	response = requests.get(url, params=payload)
	print(response.json())
	sleep(5)
