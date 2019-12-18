from app import db
from app.config import Config
import random
from sqlalchemy.ext.hybrid import hybrid_property


def id_gen():
    return random.randint(app.config["MIN_ID"], app.config["MAX_ID"])


class Quiz(db.Model):
    id_ = db.Column(db.BigInteger, primary_key=True, default=id_gen)
    name = db.Column(db.String(length=255))
    questions = db.relationship("Question", backref="quiz", lazy="dynamic")
    guesses = db.relationship("Guess", backref="quiz", lazy="dynamic")


class Question(db.Model):
    id_ = db.Column(db.BigInteger, primary_key=True, default=id_gen)
    text = db.Column(db.String(length=255))
    text_long = db.Column(db.String(length=255))
    quiz_id = db.Column(db.BigInteger, db.ForeignKey("quiz.id_"))
    answers = db.relationship("Answer", backref="question", lazy="dynamic")
    index = db.Column(db.BigInteger)


class Answer(db.Model):
    id_ = db.Column(db.BigInteger, primary_key=True, default=id_gen)
    text = db.Column(db.String(length=255))
    question_id = db.Column(db.BigInteger, db.ForeignKey("question.id_"))
    correct_answer = db.Column(db.Boolean)
    answer_guesses = db.relationship("AnswerGuess", backref="answer", lazy="dynamic")
    image = db.Column(db.String(length=255))


class Guess(db.Model):
    id_ = db.Column(db.BigInteger, primary_key=True, default=id_gen)
    quiz_id = db.Column(db.BigInteger, db.ForeignKey("quiz.id_"))
    name = db.Column(db.String(length=255))
    answer_guesses = db.relationship("AnswerGuess", backref="guess", lazy="dynamic")

    def score(self):
        result = 0
        for answer_guess in AnswerGuess.query.filter_by(guess_id=self.id_):
            if answer_guess.answer.correct_answer:
                result += 1
        return result


class AnswerGuess(db.Model):
    id_ = db.Column(db.BigInteger, primary_key=True, default=id_gen)
    guess_id = db.Column(db.BigInteger, db.ForeignKey("guess.id_"))
    answer_id = db.Column(db.BigInteger, db.ForeignKey("answer.id_"))
