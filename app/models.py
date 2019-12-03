from app import db
from app.config import Config
import random


def id_gen():
    return random.randint(Config.MIN_ID, Config.MAX_ID)


class Quiz(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, default=id_gen)
    name = db.Column(db.String(length=255))
    questions = db.relationship("Question", backref="quiz", lazy="dynamic")
    guesses = db.relationship("Guess", backref="quiz", lazy="dynamic")


class Question(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, default=id_gen)
    text = db.Column(db.String(length=255))
    quiz_id = db.Column(db.Integer, foreign_key="quiz.id_")
    answers = db.relationship("Answer", backref="question", lazy="dynamic")


class Answer(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, default=id_gen)
    text = db.Column(db.String(length=255))
    question_id = db.Column(db.Integer, foreign_key="question.id_")
    correct_answer = db.Column(db.Boolean)
    answer_guesses = db.relationship("AnswerGuess", backref="answer", lazy="dynamic")


class Guess(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, default=id_gen)
    quiz_id = db.Column(db.Integer, foreign_key="quiz.id_")
    name = db.Column(db.String(length=255))
    answer_guesses = db.relationship("AnswerGuess", backref="guess", lazy="dynamic")


class AnswerGuess(db.Model):
    id_ = db.Column(db.Integer, primary_key=True, default=id_gen)
    guess_id = db.Column(db.Integer, foreign_key="guess.id_")
    answer_id = db.Column(db.Integer, foreign_key="answer.id_")
