import requests

url = f'http://192.168.1.24/?v=high'
res = requests.get(url)
print(res)
print(res.json())
