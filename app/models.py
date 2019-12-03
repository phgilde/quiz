from app import db


class Quiz(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255))
    questions = db.relationship("Question", backref="quiz", lazy="dynamic")


class Question(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(length=255))
    quiz_id = db.Column(db.Integer, foreign_key="quiz.id_")
