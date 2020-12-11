from app import app, db
from app.models import Quiz, Answer, Question, Guess, AnswerGuess


def clear_db():
    columns = [Quiz, Answer, Question, Guess, AnswerGuess]
    for column in columns:
        entries = column.query.all()
        for entry in entries:
            db.session.delete(entry)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Quiz": Quiz,
        "Answer": Answer,
        "Question": Question,
        "Guess": Guess,
        "AnswerGuess": AnswerGuess,
        "clear_db": clear_db,
    }

