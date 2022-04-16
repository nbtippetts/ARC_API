import requests

url = "http://127.0.0.1:5000/climate/log"
payload = [
	{
		"co2": 500,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 1034,
		"humidity": 22,
		"temperature": 80
	},
	{
		"co2": 888,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 666,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 999,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 789,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 589,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 1200,
		"humidity": 20,
		"temperature": 80
	},
	{
		"co2": 1100,
		"humidity": 20,
		"temperature": 80
	},
]

for p in payload:
	response = requests.get(url, params=p)
	print(response.json())
