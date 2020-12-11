from app import app, db
from app.models import Quiz, Answer, Question, Guess, AnswerGuess


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Quiz": Quiz,
        "Answer": Answer,
        "Question": Question,
        "Guess": Guess,
        "AnswerGuess": AnswerGuess,
    }

