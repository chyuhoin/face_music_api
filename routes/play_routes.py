import json
import math
import random

from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import app, db
from models.play import Play
from models.music import Music
from sqlalchemy import func

play_field = {
    'message': fields.String,
    'id': fields.String,
    'user': fields.String,
    'count': fields.Integer,
    'music': fields.Integer,
    'skip': fields.Boolean
}


class PlayResource(Resource):
    @marshal_with(play_field)
    @jwt_required()
    def get(self, play_id):
        play = Play.query.get_or_404(play_id)
        return play

    @marshal_with(play_field)
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('music', type=int)
        parser.add_argument('skip', type=bool)
        args = parser.parse_args()

        new_count = db.session.query(func.max(Play.count)).filter(Play.user == get_jwt_identity()).scalar()
        if new_count is None:
            new_count = 0
        new_count += 1

        play = Play(
            user=get_jwt_identity(),
            count=new_count,
            music=args['music'],
            skip=args['skip']
        )
        db.session.add(play)
        db.session.commit()
        return play, 201


def clac_similarity(user_emotion, music_emotion):
    point = 0
    for key in user_emotion.keys():
        point += user_emotion[key] * music_emotion[key]
    user_norm = 0
    for value in user_emotion.values():
        user_norm += value * value
    music_norm = 0
    for value in music_emotion.values():
        music_norm += value * value
    return point / math.sqrt(user_norm * music_norm)


class Recommend(Resource):

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('emotion', type=str, required=True, help='Where is your emotion?')
        args = parser.parse_args()
        emotion = json.loads(args['emotion'])

        # 记录每首歌的七维情感倾向，使用余弦相似度进行推荐
        all_music = Music.query.all()
        best_music = []

        for music in all_music:
            music_emotion = json.loads(music.emotion)
            best_music.append((clac_similarity(emotion, music_emotion), music))

        sorted(best_music, key=lambda x: x[0], reverse=True)
        upper = max(len(best_music) // 10, 1)
        choice = random.randint(0, upper)
        return {"recommend": best_music[choice][1].id}
