from config import app, db
from routes.user_routes import UserRegistration, UserLogin, UserResource
from routes.face_routes import FaceResource, FaceExamine
from flask_restful import Api

api = Api(app)

# 添加资源到API
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserResource, '/user/<string:user_id>')

api.add_resource(FaceResource, '/face/<string:face_id>')
api.add_resource(FaceExamine, '/examine')

if __name__ == '__main__':
    db.create_all()
    app.run()