import logging
from flask_restful import abort, fields, marshal_with, reqparse, Resource
from app.models import RoomModel, NoteBookModel
from app.app import db, api
from flask import make_response
from datetime import datetime
from .utils import format_local_datetime


notebook_marshaller = {
	"notebook_id": fields.Integer,
	"title": fields.String,
	"body": fields.String,
	"publish_date": fields.String
}

notebook_parser = reqparse.RequestParser()
notebook_parser.add_argument(
	'title', type=str, help='Invalid Title', required=True)
notebook_parser.add_argument(
	'body', type=str, help='Invalid Body Text', required=True)

class NoteBook(Resource):
	@marshal_with(notebook_marshaller)
	def get(self, room_id, note_id):
		notes = NoteBookModel.query.filter_by(room_id=room_id).all()
		if not notes:
			abort(409, message="No Note")
		return notes, 200

	@marshal_with(notebook_marshaller)
	def put(self, room_id, note_id):
		args = notebook_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		pub_date=format_local_datetime()
		notes = NoteBookModel(
			title=args['title'], body=args['body'], publish_date=pub_date, room=rooms)
		db.session.add(notes)
		db.session.commit()
		return notes, 201

	@marshal_with(notebook_marshaller)
	def patch(self, room_id, note_id):
		args = notebook_parser.parse_args()
		rooms = RoomModel.query.filter_by(id=room_id).first()
		if not rooms:
			abort(409, message="Room {} does not exist".format(room_id))
		notes = NoteBookModel.query.filter_by(
			notebook_id=note_id, room=rooms).first()
		if not notes:
			abort(409, message="Note {} doesn't exist, cannot update.".format(note_id))
		notes.title = args['title']
		notes.body = args['body']
		db.session.add(notes)
		db.session.commit()
		return notes, 201

	@marshal_with(notebook_marshaller)
	def delete(self, room_id, note_id):
		notes = NoteBookModel.query.filter_by(notebook_id=note_id).first()
		if not notes:
			abort(409, message="Note {} doesn't exist, cannot delete.".format(note_id))
		db.session.delete(notes)
		db.session.commit()
		return 'SUCCESS', 204


# Define parser and request args
notebook_date_parser = reqparse.RequestParser()
notebook_date_parser.add_argument(
	'noteDate', type=str, help='Invalid Date', required=True)


class Notes(Resource):
	@marshal_with(notebook_marshaller)
	def get(self, room_id):
		args = notebook_date_parser.parse_args()
		x = args['noteDate'].split(".")
		local_time = datetime.strptime(x[0], '%Y-%m-%dT%H:%M:%S')
		local_time = local_time.strftime("%d %b, %I:%M %p")
		pub_date = local_time.split(",")
		notes = NoteBookModel.query.filter(
			NoteBookModel.publish_date.startswith(pub_date[0]), NoteBookModel.room_id == room_id).all()
		if not notes:
			abort(409, message="No Note")
		return notes, 200

api.add_resource(Notes, '/room/<int:room_id>/notes')
api.add_resource(NoteBook, '/room/<int:room_id>/note/<int:note_id>')
