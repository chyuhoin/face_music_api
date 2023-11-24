from config import db


class Play(db.Model):

    __tablename__ = 't_face'

    id = db.Column(db.String, primary_key=True, default=db.text("gen_random_uuid()"), nullable=False)
    user = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    music = db.Column(db.Integer, nullable=False)
    skip = db.Column(db.Boolean, nullable=False)
