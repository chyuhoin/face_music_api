from config import db

class User(db.Model):

    __tablename__ = 't_user'

    id = db.Column(db.String, primary_key=True, default=db.text("gen_random_uuid()"), nullable=False)
    phone = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean, default=True, nullable=False)
    address = db.Column(db.String(255))
    style = db.Column(db.String(255))
    emotion = db.Column(db.Integer)
    level = db.Column(db.Boolean, default=False, nullable=False)
    uid = db.Column(db.String(255))