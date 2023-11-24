from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import app, db
from models.music import Music


music_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'emotion': fields.String,
    'style': fields.String,
}


class MusicResource(Resource):
    @marshal_with(music_fields)
    @jwt_required()
    def get(self, music_id):
        music = Music.query.get(music_id)
        if music:
            return music
        else:
            return {'message': 'Music not found'}, 404

    @marshal_with(music_fields)
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)
        parser.add_argument('emotion', type=str)
        parser.add_argument('style', type=str)
        args = parser.parse_args()

        music = Music(**args)
        db.session.add(music)
        db.session.commit()
        return music, 201

    @marshal_with(music_fields)
    @jwt_required()
    def put(self, music_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('emotion', type=str)
        parser.add_argument('style', type=str)
        args = parser.parse_args()

        music = Music.query.get(music_id)
        if music:
            for key, value in args.items():
                if value is not None:
                    setattr(music, key, value)
            db.session.commit()
            return music
        else:
            return {'message': 'Music not found'}, 404

    @jwt_required()
    def delete(self, music_id):
        music = Music.query.get(music_id)
        if music:
            db.session.delete(music)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'Music not found'}, 404
