from app import db
from app.quiz import answers


class Quiz(db.Model):
    name = db.Column(db.String(length=255))
    correct_answers = db.Column(db.String(length=len(answers)*2))
    id_ = db.Column(db.Integer, primary_key=True)
    answers = db.relationship("Answer", backref="quiz", lazy="dynamic")


class Answer(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=255))
    answers = db.Column(db.String(length=len(answers)*2))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id_"))

    def score(self):
        answers = self.answers.split(" ")
        correct_answers = self.quiz.correct_answers.split(" ")

        return sum([1 if answer == correct_answer
                    else 0 for answer, correct_answer
                    in zip(answers, correct_answers)])
