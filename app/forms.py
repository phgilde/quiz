from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class QuizForm(FlaskForm):
    name = StringField("name")
    answers = StringField("answers")
    submit = SubmitField("Abschicken")
