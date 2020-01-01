from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

from app import app, db
from app.forms import QuizForm
from app.models import Quiz, Question, Answer, Guess, AnswerGuess
from app.quiz import answers, questions, questiontexts_name, questiontexts_new


@app.route("/index")
@app.route("/")
def index():
    if request.cookies.get("quiz"):
        return redirect(url_for("quiz", id_=request.cookies.get("quiz")))
    return render_template("index.html")


@app.route("/newquiz", methods=["GET", "POST"])
def newquiz():
    form = QuizForm()

    if form.validate_on_submit():
        app.logger.info(app.config["SQLALCHEMY_DATABASE_URI"])
        flash("Quiz abgeschickt!")
        # get answers
        name = form.name.data
        answers_form = form.answers.data.split(sep=";")

        # new quiz entry
        quiz = Quiz(name=name)
        db.session.add(quiz)
        for i in range(len(answers_form)):
            question = Question(text=questions[i], quiz=quiz, index=i, text_long=questiontexts_name[i],)
            for j in range(len(answers[i])):
                db.session.add(
                    Answer(text=answers[i][j], question=question, correct_answer=(answers[i][j] == answers_form[i]),)
                )
            if answers_form[i] not in answers[i]:
                db.session.add(Answer(text=answers_form[i], question=question, correct_answer=True,))
        db.session.commit()
        id_ = quiz.id_
        resp = make_response(redirect(url_for("quiz", id_=id_)))
        resp.set_cookie("quiz", str(id_))
        resp.set_cookie(str(id_), "True")

        return resp

    return render_template("newquiz.html", form=form, questions=questiontexts_new, answers=answers,)


@app.route("/q/<id_>", methods=["GET", "POST"])
def quiz(id_):
    if not Quiz.query.get(id_):
        response = make_response(render_template("noquiz.html"))
        # remove cookie if quiz doesnt exist
        if request.cookies.get("quiz") == id_:
            response.set_cookie("quiz", "", expires=0)
        return response
    form = QuizForm()
    quiz = Quiz.query.get(id_)
    if form.validate_on_submit():
        flash("Quiz abgeschickt!")
        name = form.name.data
        answers_form = form.answers.data.split()

        guess = Guess(name=name, quiz=Quiz.query.get(id_))
        db.session.add(guess)
        for i in range(len(answers_form)):
            db.session.add(
                AnswerGuess(
                    guess=guess,
                    answer=Answer.query.filter(
                        db.and_(Answer.question.has(quiz=quiz), Answer.text == answers[i][int(answers_form[i])],)
                    ).first(),
                )
            )
        db.session.commit()

        resp = make_response(redirect(url_for("quizanswers", id_=id_)))
        resp.set_cookie(id_, str(guess.id_))
        return resp

    if request.cookies.get(id_):
        return redirect(url_for("quizanswers", id_=id_))
    else:
        return render_template(
            "quiz.html",
            form=form,
            questions=[question.text_long.format(quiz.name) for question in quiz.questions],
            answers=[[answer.text for answer in question.answers] for question in quiz.questions],
            quiz_id=request.cookies.get("quiz"),
            name=quiz.name,
            title=f"Wie gut kennst du {quiz.name}?",
        )


@app.route("/a/<id_>")
def quizanswers(id_):
    if not request.cookies.get(id_):
        return redirect(url_for("quiz", id_=id_))

    id_ = int(id_)
    quiz = Quiz.query.get(id_)
    if not quiz:
        return render_template("noquiz.html", id_=request.cookies.get("quiz"))

    questions_corr, answers_corr = [], []

    for q in sorted(quiz.questions, key=lambda x: x.index):
        for a in q.answers:
            if a.correct_answer:
                questions_corr.append(q.text)
                answers_corr.append(a.text)

    if request.cookies.get("quiz") == str(id_):
        return render_template(
            "quizanswers.html",
            guesses=sorted(quiz.guesses, key=lambda x: x.score(), reverse=True),
            correct_answers=zip(questions_corr, answers_corr, [None for i in range(len(answers_corr))],),
            curr_id=id_,
            name=quiz.name,
            max_score=len(questions),
            quiz_id=request.cookies.get("quiz"),
        )
    else:
        user_guess = Guess.query.get(int(request.cookies.get(str(id_)) or 0))
        user_answers = []
        for answer in sorted(user_guess.answer_guesses, key=lambda x: x.answer.question.index):
            user_answers.append(answer.answer.text)
        return render_template(
            "quizanswers.html",
            guesses=sorted(quiz.guesses, key=lambda x: x.score(), reverse=True),
            correct_answers=zip(questions_corr, answers_corr, user_answers),
            quiz_id=request.cookies.get("quiz"),
            curr_id=id_,
            name=quiz.name,
            max_score=len(questions),
        )
