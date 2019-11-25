from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class QuizForm(FlaskForm):
    name = StringField("Dein Name", validators=[DataRequired(), Length(max=15)])
    # submit = SubmitField("Jetzt Quiz erstellen!")


def gen_quizform(questions, answers, submit_text):
    class QuizFormClone(QuizForm):
        submit = SubmitField(submit_text)

    for i in range(len(questions)):
        field = RadioField(label=questions[i],
                           choices=[(str(x), answers[i][x])
                                    for x in range(len(answers[i]))])
        setattr(QuizFormClone, f"field{i}", field)
    # setattr(QuizFormClone, "submit", SubmitField(submit))
    return QuizFormClone()
