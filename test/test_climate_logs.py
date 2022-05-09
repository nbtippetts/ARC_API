import requests
from time import sleep
import random

url = "http://localhost:5000/climate/log"
while True:
	co2 = random.randint(900, 1300)
	hum = random.randint(30, 55)
	temp = random.randint(20, 35)
	payload = {
		"co2": co2,
		"humidity": hum,
		"temperature": temp
	}
	response = requests.get(url, params=payload)
	print(response.json())
	sleep(5)
