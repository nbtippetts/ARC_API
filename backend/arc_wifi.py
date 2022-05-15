import os
import subprocess
import sys
def scan_wifi(ssid,pw):
	#return all the available network
	networks = subprocess.check_output(['nmcli', 'dev', 'wifi','list'])
	decoded_networks = networks.decode('utf-8')
	print(decoded_networks)
def connect_wifi(ssid,pw):
	try:
		os.system(f"sudo nmcli dev wifi connect {ssid} password {pw}")
	except:
		raise
if __name__ == "__main__":
	ssid = str(sys.argv[1])
	pw = str(sys.argv[2])
	print(ssid)
	print(pw)
	scan_wifi()
	connect_wifi(ssid,pw)