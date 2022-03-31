import requests

url = "http://127.0.0.1:5000/ap_jobs"

response = requests.get(url)
print(response.text)
