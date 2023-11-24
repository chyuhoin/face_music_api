from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import app, db
from models.feedback import Feedback


feedback_fields = {
    'id': fields.String,
    'user': fields.String,
    'count': fields.Integer,
    'score': fields.Integer,
    'feedback': fields.String
}


class FeedbackResource(Resource):
    @marshal_with(feedback_fields)
    def get(self, feedback_id):
        feedback = Feedback.query.get(feedback_id)
        if feedback:
            return feedback
        else:
            return {'message': 'Feedback not found'}, 404

    @marshal_with(feedback_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str, required=True, help='User is required')
        parser.add_argument('count', type=int, required=True, help='Count is required')
        parser.add_argument('score', type=int, required=True, help='Score is required')
        parser.add_argument('feedback', type=str, required=True, help='Feedback is required')
        args = parser.parse_args()

        feedback = Feedback(user=args['user'], count=args['count'], score=args['score'], feedback=args['feedback'])
        db.session.add(feedback)
        db.session.commit()
        return feedback, 201

    @marshal_with(feedback_fields)
    def put(self, feedback_id):
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return {'message': 'Feedback not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('user', type=str)
        parser.add_argument('count', type=int)
        parser.add_argument('score', type=int)
        parser.add_argument('feedback', type=str)
        args = parser.parse_args()

        for key, value in args.items():
            if value is not None:
                setattr(feedback, key, value)

        db.session.commit()
        return feedback

    def delete(self, feedback_id):
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return {'message': 'Feedback not found'}, 404

        db.session.delete(feedback)
        db.session.commit()
        return {'message': 'Feedback deleted'}, 200
