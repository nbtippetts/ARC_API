from app.app import db
from app.models import IPModel, ClimateScheduleLogModel
from tzlocal import get_localzone
from datetime import datetime
import requests
from requests.adapters import HTTPAdapter
import logging

def get_local_time():
	local_tz = get_localzone()
	now_dt = datetime.now()
	now_local_dt = now_dt.replace(tzinfo=local_tz)
	local_time = now_local_dt.strftime("%I:%M %p")
	print(local_time)
	return local_time
def get_local_datetime():
	local_tz = get_localzone()
	now_dt = datetime.now()
	now_local_dt = now_dt.replace(tzinfo=local_tz)
	print(now_local_dt)
	return now_local_dt


def is_time_between(begin_time, end_time):
	local_tz = get_localzone()
	now_dt = datetime.now().time()
	now_local_dt = now_dt.replace(tzinfo=local_tz)
	if begin_time < end_time:
		return now_local_dt >= begin_time and now_local_dt <= end_time
	else:  # crosses midnight
		return now_local_dt >= begin_time or now_local_dt <= end_time

def test_start_task(*args):
	print(args)
	logging.info(args)
	ip_state = IPModel.query.filter_by(ip=args[1]).first()
	if ip_state.state == False:
		logs = ClimateScheduleLogModel(name=ip_state.name, start_time=get_local_time(), end_time=get_local_time(), end_time_flag=True, IP=ip_state)
		db.session.add(logs)
		db.session.commit()
		ip_state.state=True
		db.session.add(ip_state)
		db.session.commit()
		return args

def test_end_task(*args):
	print(args)
	logging.info(args)
	ip_state = IPModel.query.filter_by(ip=args[1]).first()
	logs = ClimateScheduleLogModel.query.filter_by(IP=ip_state).order_by(ClimateScheduleLogModel.climate_schedule_log_id.desc()).first()
	if logs.end_time_flag:
		logs.end_time_flag = False
		logs.end_time = get_local_time()
		db.session.add(logs)
		db.session.commit()
		ip_state.state = False
		db.session.add(ip_state)
		db.session.commit()
		return args


def start_task(*args):
	print(args)
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=5))
	url = f'http://{args[1]}/?v={args[0]}'
	res = s.get(url,timeout=5)
	logging.info(res)
	if res.status_code == 200:
		ip_state = IPModel.query.filter_by(ip=args[1]).first()
		if ip_state.state == False:
			logs = ClimateScheduleLogModel(name=ip_state.name, start_time=get_local_time(
			), end_time=get_local_time(), end_time_flag=True, IP=ip_state)
			db.session.add(logs)
			db.session.commit()
			ip_state.state = True
			db.session.add(ip_state)
			db.session.commit()
			return res
	else:
		print(res)
		return res
	# print(url)


def end_task(*args):
	print(args)
	s = requests.Session()
	s.mount('http://', HTTPAdapter(max_retries=5))
	url = f'http://{args[1]}/?v={args[0]}'
	res = s.get(url, timeout=5)
	if res.status_code == 200:
		ip_state = IPModel.query.filter_by(ip=args[1]).first()
		logs = ClimateScheduleLogModel.query.filter_by(IP=ip_state).order_by(
			ClimateScheduleLogModel.climate_schedule_log_id.desc()).first()
		if logs.end_time_flag:
			logs.end_time_flag = False
			logs.end_time = get_local_time()
			db.session.add(logs)
			db.session.commit()
			ip_state.state = False
			db.session.add(ip_state)
			db.session.commit()
			return res
	else:
		print(res)
		return res


def check_ip_state(ip):
	end_task('high', ip.ip)
	ip.state = False
	db.session.add(ip)
	db.session.commit()
	return 'SUCCESS'
