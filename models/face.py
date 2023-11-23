from config import db


class Face(db.Model):

    __tablename__ = 't_face'

    id = db.Column(db.String, primary_key=True, default=db.text("gen_random_uuid()"), nullable=False)
    user = db.Column(db.String)
    count = db.Column(db.Integer)
    score = db.Column(db.String(255))
    gmt_create = db.Column(db.Date, default=db.text("now()"), nullable=False)
