from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class QuizForm(FlaskForm):
    name = StringField("name")
    answers = StringField("answers")
    submit = SubmitField("Abschicken")

