def deploy():
	"""Run deployment tasks."""
	from app.app import create_app, db
	from flask_migrate import upgrade, migrate, init, stamp
	from app.models import RoomModel, IPModel,ClimateScheduleModel,ClimateIntervalModel,ClimateModel,ClimateDayNightModel,ClimateScheduleLogModel,ClimateLogModel,NoteBookModel

	app = create_app()
	app.app_context().push()

	# create database and tables
	db.create_all()

	# migrate database to latest revision
	stamp()
	migrate()
	upgrade()


deploy()
