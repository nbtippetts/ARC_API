from app.app import db
from datetime import datetime
from tzlocal import get_localzone
tz = get_localzone()
print(tz)
LOCAL_DT = datetime.now()
print(LOCAL_DT)
LOCAL_DT = LOCAL_DT.replace(tzinfo=tz)
print(LOCAL_DT)

class RoomModel(db.Model):
	__tablename__ = 'room'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	climate_schedule = db.relationship('ClimateScheduleModel', cascade='all, delete', backref='room', lazy='joined')
	climate_interval = db.relationship('ClimateIntervalModel', cascade='all, delete', backref='room', lazy='joined')
	climate = db.relationship('ClimateModel', cascade='all, delete', backref='room', lazy='joined')
	notebook = db.relationship('NoteBookModel', cascade='all, delete', backref='room', lazy='joined')
	ip = db.relationship('IPModel', cascade='all, delete',backref='room', lazy='joined')
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class IPModel(db.Model):
	__tablename__ = 'IP'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	state = db.Column(db.Boolean, default=False, nullable=False)
	ip = db.Column(db.String(20), default='False', nullable=False)
	climate_schedule = db.relationship(
		'ClimateScheduleModel', cascade='all, delete', backref='IP', lazy='joined')
	climate_interval = db.relationship(
		'ClimateIntervalModel', cascade='all, delete', backref='IP', lazy='joined')
	climate_schedule_log = db.relationship('ClimateScheduleLogModel', backref='IP',lazy='select', order_by='ClimateScheduleLogModel.climate_schedule_log_id.desc()')
	climate = db.relationship('ClimateModel', cascade='all, delete', backref='IP', lazy='joined')
	climate_log = db.relationship('ClimateLogModel', backref='IP',lazy='select', order_by='ClimateLogModel.climate_log_id.desc()')
	climate_reads = db.relationship(
		'ClimateLiveDataModel', backref='IP', lazy='select')
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class ClimateScheduleModel(db.Model):
	__tablename__ = 'climate_schedule'
	climate_schedule_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.String(100), nullable=False)
	end_time = db.Column(db.String(100), nullable=False)
	how_often = db.Column(db.String(20), nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class ClimateIntervalModel(db.Model):
	__tablename__ = 'climate_interval'
	climate_interval_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	interval_hour = db.Column(db.Integer, default=0, nullable=False)
	interval_minute = db.Column(db.Integer, default=0, nullable=False)
	duration_hour = db.Column(db.Integer, default=0, nullable=False)
	duration_minute = db.Column(db.Integer, default=0, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class ClimateModel(db.Model):
	__tablename__ = 'climate'
	climate_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	co2_parameters = db.Column(db.Integer, nullable=False)
	humidity_parameters = db.Column(db.Integer, nullable=False)
	temperature_parameters = db.Column(db.Integer, nullable=False)
	buffer_parameters = db.Column(db.Integer, default=0, nullable=False)
	co2_buffer_parameters = db.Column(db.Integer, default=0, nullable=False)
	co2_relay_ip = db.Column(db.String(20), nullable=False)
	humidity_relay_ip = db.Column(db.String(20), nullable=False)
	exhaust_relay_ip = db.Column(db.String(20), nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	climate_day_night = db.relationship(
		'ClimateDayNightModel', cascade='all, delete', backref='climate', lazy='joined')
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class ClimateDayNightModel(db.Model):
	__tablename__ = 'climate_day_night'
	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	climate_start_time = db.Column(db.Time, default=None)
	climate_end_time = db.Column(db.Time, default=None)
	climate_id = db.Column(db.Integer, db.ForeignKey('climate.climate_id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class ClimateScheduleLogModel(db.Model):
	__tablename__ = 'climate_schedule_log'
	climate_schedule_log_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	start_time = db.Column(db.String(100), nullable=False)
	end_time = db.Column(db.String(100), nullable=False)
	end_time_flag = db.Column(db.Boolean, default=False, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class ClimateLogModel(db.Model):
	__tablename__ = 'climate_log'
	climate_log_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	co2 = db.Column(db.Integer, nullable=False)
	humidity = db.Column(db.Integer, nullable=False)
	temperature = db.Column(db.Integer, nullable=False)
	vpd = db.Column(db.Float, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)
class ClimateLiveDataModel(db.Model):
	__tablename__ = 'climate_live_reads'
	id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	co2 = db.Column(db.Integer, nullable=False)
	humidity = db.Column(db.Integer, nullable=False)
	temperature = db.Column(db.Integer, nullable=False)
	vpd = db.Column(db.Float, nullable=False)
	ip_id = db.Column(db.Integer, db.ForeignKey('IP.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)


class NoteBookModel(db.Model):
	__tablename__ = 'notebook'
	notebook_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
	title = db.Column(db.String(100), nullable=False)
	body = db.Column(db.String(800), nullable=False)
	publish_date = db.Column(db.String(100), nullable=False)
	room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
	timestamp = db.Column(
		db.DateTime, default=LOCAL_DT, onupdate=LOCAL_DT
	)
