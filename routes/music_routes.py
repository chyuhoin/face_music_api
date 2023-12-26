from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import app, db
from models.music import Music
import json


music_fields = {
    'message': fields.String,
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


class AddMusic(Resource):
    @marshal_with(music_fields)
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('emotion', type=str, required=True)
        parser.add_argument('style', type=str, required=True)
        args = parser.parse_args()

        music = Music(**args)
        db.session.add(music)
        db.session.commit()
        return music, 201


class MusicIds(Resource):
    def get(self):
        music_list = Music.query.order_by(Music.id.asc()).all()
        res = ""
        for music in music_list:
            res += str(music.id) + ','
        return {"ids": res[0: -1]}


class MusicData(Resource):
    @jwt_required()
    def get(self):
        all_music = Music.query.all()
        count = dict()
        total = 0
        for music in all_music:
            emotion = json.loads(music.emotion)
            print(emotion)
            for key in emotion.keys():
                total += emotion[key]
                count[key] = emotion[key] + count.get(key, 0.0)
        for key in count.keys():
            count[key] /= total
        return count


class MusicList(Resource):
    def get(self):
        music_list = Music.query.order_by(Music.id.asc()).all()
        res = []
        for music in music_list:
            cov = dict()
            cov['id'] = music.id
            cov['name'] = music.name
            e = json.loads(music.emotion)
            cov['emotion'] = [e['anger'], e['disgust'], e['fear'], e['happiness'], e['neutral'], e['sadness'], e['surprise']]
            res.append(cov)
        return res


class MusicSearch(Resource):
    def get(self, music_name):
        music_list = Music.query.filter(Music.name.like(f'%{music_name}%')).order_by(Music.id.asc()).all()
        res = []
        for music in music_list:
            cov = dict()
            cov['id'] = music.id
            cov['name'] = music.name
            e = json.loads(music.emotion)
            cov['emotion'] = [e['anger'], e['disgust'], e['fear'], e['happiness'], e['neutral'], e['sadness'], e['surprise']]
            res.append(cov)
        return res
