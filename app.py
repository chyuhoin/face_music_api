from config import app, db
from routes.user_routes import UserRegistration, UserLogin, UserResource, UserList, MyInfo
from routes.face_routes import FaceResource, FaceExamine, FaceData, FaceDay
from routes.music_routes import MusicResource, AddMusic, MusicIds, MusicData, MusicList, MusicSearch
from routes.play_routes import PlayResource, Recommend
from routes.feedback_routes import FeedbackResource, AddFeedback, FeedbackList
from flask_restful import Api

api = Api(app)

# 添加资源到API
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserResource, '/user/<string:user_id>')
api.add_resource(UserList, '/userList')
api.add_resource(MyInfo, '/myInfo')

api.add_resource(FaceResource, '/face/<string:face_id>')
api.add_resource(FaceExamine, '/examine')
api.add_resource(FaceData, '/face/data')
api.add_resource(FaceDay, '/face/day')

api.add_resource(MusicResource, '/music/<string:music_id>')
api.add_resource(AddMusic, '/add/music')
api.add_resource(MusicIds, '/musicIds')
api.add_resource(MusicData, '/music/data')
api.add_resource(MusicList, '/musicList')
api.add_resource(MusicSearch, '/musicSearch/<string:music_name>')

api.add_resource(PlayResource, '/play/<string:play_id>')
api.add_resource(Recommend, '/recommend')

api.add_resource(FeedbackResource, '/feedback/<string:feedback_id>')
api.add_resource(AddFeedback, '/add/feedback')
api.add_resource(FeedbackList, '/feedbackList')

if __name__ == '__main__':
    db.create_all()
    app.run()