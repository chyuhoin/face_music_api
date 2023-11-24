from config import db


class Music(db.Model):

    __tablename__ = 't_music'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255))
    emotion = db.Column(db.String(255))
    style = db.Column(db.String(255))
