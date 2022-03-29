from flask_restful import Api
from tzlocal import get_localzone
from datetime import datetime
import urllib.parse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import os
from services import create_app

arc_app = create_app()
api = Api(arc_app)

tz = get_localzone()
print(tz)
LOCAL_DT = datetime.now()
print(LOCAL_DT)
LOCAL_DT = LOCAL_DT.replace(tzinfo=tz)
print(LOCAL_DT)

jobstores = {
	# 'default': SQLAlchemyJobStore(url="mysql+pymysql://root:{}@localhost/arc_db".format( urllib.parse.quote_plus("@Wicked2009")))
	'default': SQLAlchemyJobStore(url='mariadb+pymysql://{}:{}@{}/{}'.format(
		os.getenv('DB_USER', 'flask'),
		os.getenv('DB_PASSWORD', ''),
		os.getenv('DB_HOST', 'mariadb'),
		os.getenv('DB_NAME', 'flask')
	))
}
executors = {
	'default': ThreadPoolExecutor(20),
	'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
	'coalesce': False,
	'max_instances': 3
}

appscheduler = BackgroundScheduler(daemon=True, jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=tz)
appscheduler.start()



from services.arc_room import RoomIP, RoomList, IPList, IPLogs, AddIP
from services.arc_schedule import RelaySchedule, RelayScheduleList, RoomRelayScheduleList
from services.arc_interval import RelayInterval, RelayIntervalList, RoomRelayIntervalList
from services.arc_climate import ClimateParameters, ClimateParametersIPList, ClimateParametersList, Climate, ClimateLog
from services.arc_relay import RelayControl





# api.add_resource(Room, '/room/<int:room_id>')
api.add_resource(RoomList, '/rooms')

api.add_resource(AddIP, '/ip')
api.add_resource(RoomIP, '/room/<int:room_id>/ip/<int:ip_id>')
api.add_resource(IPLogs, '/room/<int:room_id>/ips')
api.add_resource(IPList, '/all_ips')

api.add_resource(RelayControl, '/relay_control/')

api.add_resource(RelaySchedule, '/room/<int:room_id>/relayschedule/<int:schedule_id>')
api.add_resource(RoomRelayScheduleList, '/room/<int:room_id>/relayschedule')
api.add_resource(RelayScheduleList, '/relayschedule')

api.add_resource(RelayInterval, '/room/<int:room_id>/relayinterval/<int:interval_id>')
api.add_resource(RoomRelayIntervalList, '/room/<int:room_id>/relayinterval')
api.add_resource(RelayIntervalList, '/relayinterval')

api.add_resource(ClimateParameters,'/room/<int:room_id>/climate/<int:climate_parameter_id>')
api.add_resource(ClimateParametersIPList, '/room/<int:room_id>/climate_ips')
api.add_resource(ClimateParametersList,'/room/<int:room_id>/climate')

api.add_resource(Climate, '/climate')
api.add_resource(ClimateLog, '/climate/log')

if __name__ == '__main__':
	db.create_all()
	app.run(host='0.0.0.0')