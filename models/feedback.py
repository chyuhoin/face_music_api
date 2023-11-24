from config import db


class Feedback(db.Model):
    __tablename__ = 't_feedback'

    id = db.Column(db.String, primary_key=True, default=db.text("gen_random_uuid()"), nullable=False)
    user = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.Text)
    