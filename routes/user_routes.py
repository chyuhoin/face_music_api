from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import app, db
from models.user import User
from datetime import timedelta


user_fields = {
    'message': fields.String,
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


def get_args(parser, is_new: bool):
    parser.add_argument('phone', type=str, required=is_new)
    parser.add_argument('password', type=str, required=is_new)
    parser.add_argument('nickname', type=str, required=is_new)
    parser.add_argument('age', type=int)
    parser.add_argument('gender', type=bool)
    parser.add_argument('address', type=str)
    parser.add_argument('style', type=str)
    parser.add_argument('emotion', type=int)
    parser.add_argument('level', type=bool)
    parser.add_argument('uid', type=str, required=is_new)
    return parser.parse_args()


class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user

    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        args = get_args(parser, True)

        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        parser = reqparse.RequestParser()
        args = get_args(parser, False)

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
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        args = get_args(parser, True)

        user = User(**args)
        db.session.add(user)
        db.session.commit()
        return user, 201


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        current_user = User.query.filter_by(phone=data['phone']).first()
        if not current_user:
            return {'message': 'User doesn\'t exist'}

        if data['password'] == current_user.password:
            access_token = create_access_token(identity=current_user.id, expires_delta=timedelta(days=1))
            return {
                'message': 'Logged in as {}'.format(current_user.phone),
                'nickname': current_user.nickname,
                'uid': current_user.uid,
                'access_token': access_token,
                'level': current_user.level
            }
        else:
            return {'message': 'Wrong credentials'}


class UserList(Resource):
    def get(self):
        user_list = User.query.order_by(User.id.asc()).all()
        res = []
        for user in user_list:
            cov = dict()
            cov['id'] = str(user.id)
            cov['phone'] = user.phone
            cov['password'] = user.password
            cov['nickname'] = user.nickname
            cov['level'] = user.level
            res.append(cov)
        return res


class MyInfo(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def post(self):
        user = User.query.get_or_404(get_jwt_identity())
        return user
