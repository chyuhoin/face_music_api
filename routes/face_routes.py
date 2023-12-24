import werkzeug, json
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import app, db
from models.face import Face
from utils.face_utils import ask_faceplus
from sqlalchemy import func


face_fields = {
    'message': fields.String,
    'id': fields.String,
    'user': fields.String,
    'count': fields.Integer,
    'score': fields.String,
    'gmt_create': fields.String
}


class FaceResource(Resource):
    @marshal_with(face_fields)
    @jwt_required()
    def get(self, face_id):
        face = Face.query.get(face_id)
        if face:
            return face
        else:
            return {'message': 'Face not found'}, 404

    @marshal_with(face_fields)
    def put(self, face_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str)
        parser.add_argument('count', type=int)
        parser.add_argument('score', type=str)
        args = parser.parse_args()

        face = Face.query.get(face_id)
        if face:
            for key, value in args.items():
                if value is not None:
                    setattr(face, key, value)
            db.session.commit()
            return face
        else:
            return {'message': 'Face not found'}, 404

    def delete(self, face_id):
        face = Face.query.get(face_id)
        if face:
            db.session.delete(face)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'Face not found'}, 404


class FaceExamine(Resource):
    @marshal_with(face_fields)
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)
        args = parser.parse_args()

        new_count = db.session.query(func.max(Face.count)).filter(Face.user == get_jwt_identity()).scalar()
        if new_count is None:
            new_count = 0
        new_count += 1

        face_img = args['file']
        result: dict = ask_faceplus(face_img.stream.read())

        if not result.get("faces"):
            return {"message: No face"}, 200

        face = Face(
            user=get_jwt_identity(),
            count=new_count,
            score=json.dumps(result.get("faces")[0].get("attributes").get("emotion"))
        )
        db.session.add(face)
        db.session.commit()
        return face, 201


class FaceData(Resource):
    @jwt_required()
    def get(self):
        all_face = Face.query.all()
        count = dict()
        total = 0
        for face in all_face:
            emotion = json.loads(face.score)
            for key in emotion.keys():
                total += emotion[key]
                count[key] = emotion[key] + count.get(key, 0.0)
        for key in count.keys():
            count[key] /= total
        return count


class FaceDay(Resource):
    @jwt_required()
    def get(self):
        result = db.session.query(Face.gmt_create, func.string_agg(Face.score, '|')).group_by(Face.gmt_create).order_by(Face.gmt_create).all()
        date_list = []
        count_list = []
        emotion_result = dict()
        for rec in result:
            date_list.append(str(rec[0]))
            total = 0
            count = dict()
            emotion_list = rec[1].split('|')
            for e in emotion_list:
                emotion = json.loads(e)
                for key in emotion.keys():
                    total += emotion[key]
                    count[key] = emotion[key] + count.get(key, 0.0)
            for key in count.keys():
                count[key] = count[key] * 100 / total
            count_list.append(count)
        for cnt in count_list:
            for key in cnt.keys():
                if emotion_result.get(key) is None:
                    emotion_result[key] = []
                emotion_result[key].append(cnt[key])
        return {'date': date_list, 'emotion': emotion_result}
