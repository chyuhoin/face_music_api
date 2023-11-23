from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import app, db
from models.user import User

user_fields = {
    'id': fields.String,
    'phone': fields.String,
    'password': fields.String,
    'nickname': fields.String,
    'age': fields.Integer,
    'gender': fields.Boolean,
    'address': fields.String,
    'style': fields.String,
    'emotion': fields.Integer,
    'level': fields.Boolean,
    'uid': fields.String
}

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('nickname', type=str)
        parser.add_argument('age', type=int)
        parser.add_argument('gender', type=bool)
        parser.add_argument('address', type=str)
        parser.add_argument('style', type=str)
        parser.add_argument('emotion', type=int)
        parser.add_argument('level', type=bool)
        parser.add_argument('uid', type=str, required=True)
        args = parser.parse_args()

        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('phone', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('nickname', type=str)
        parser.add_argument('age', type=int)
        parser.add_argument('gender', type=bool)
        parser.add_argument('address', type=str)
        parser.add_argument('style', type=str)
        parser.add_argument('emotion', type=int)
        parser.add_argument('level', type=bool)
        parser.add_argument('uid', type=str)
        args = parser.parse_args()

        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()
        return user

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserRegistration(Resource):
    def post(self):
        return UserResource.post()

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        current_user = User.query.filter_by(phone=data['phone']).first()
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['phone'])}

        if data['password'] == current_user.password:
            access_token = create_access_token(identity=data['phone'])
            return {
                'message': 'Logged in as {}'.format(current_user.phone),
                'access_token': access_token
            }
        else:
            return {'message': 'Wrong credentials'}