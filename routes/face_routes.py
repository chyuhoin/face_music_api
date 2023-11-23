import werkzeug, json
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import app, db
from models.face import Face
from utils.face_utils import ask_faceplus

face_fields = {
    'id': fields.String,
    'user': fields.String,
    'count': fields.Integer,
    'score': fields.String,
    'gmt_create': fields.String(attribute=lambda x: x.gmt_create.strftime('%Y-%m-%d, %H:%M:%S'))
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
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()

        face_img = args['file']
        result: dict = ask_faceplus(face_img.stream.read())

        if result.get("faces") is None:
            return {"Message: No face"}, 403

        face = Face(
            user=get_jwt_identity(),
            count=1,
            score=json.dumps(result.get("faces")[0].get("attributes").get("emotion"))
        )
        db.session.add(face)
        db.session.commit()
        return face, 201
