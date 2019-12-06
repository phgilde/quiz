from random import randint

from flask import (flash, make_response, redirect, render_template, request,
                   url_for)

from app import app, db
from app.forms import QuizForm
from app.models import Quiz, Question, Answer, Guess, AnswerGuess
from app.quiz import answers, questions, questiontexts_name, questiontexts_new
from app.config import Config


@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html", id_=request.cookies.get("quiz"))


@app.route("/newquiz", methods=["GET", "POST"])
def newquiz():
    form = QuizForm()

    if form.validate_on_submit():
        flash("quiz abgeschickt!")
        # get answers
        name = form.name.data
        answers_form = form.answers.data.split()

        # if quiz already exsists
        if request.cookies.get("quiz"):
            if Quiz.query.get(request.cookies.get("quiz")):
                flash("Quiz geändert!")
                quiz = Quiz.query.get(request.cookies.get("quiz"))
                quiz.name = name
                for i in range(len(answers_form)):
                    for j in range(len(answers[i])):
                        Answer.query.filter(db.and_(text == answers[i][j], question.quiz == quiz)).first().correct_answer = (j == answers_form[i])
                db.session.commit()
                redirect(url_for("index"))
        else:
            # new quiz entry
            quiz = Quiz(name=name)
            db.session.add(quiz)
            for i in range(len(answers_form)):
                question = Question(text=questions[i], quiz=quiz, index=i)
                for j in range(len(answers[i])):
                    db.session.add(Answer(text=answers[i][j], question=question, correct_answer=(j == int(answers_form[i]))))
            db.session.commit()
            id_ = quiz.id_
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("quiz", str(id_))
            resp.set_cookie(str(id_), "True")

            return resp

    return render_template("newquiz.html", form=form,
                           questions=questiontexts_new,
                           answers=answers, id_=request.cookies.get("quiz"))


@app.route("/q/<id_>", methods=["GET", "POST"])
# @app.route("/quiz/<id_>", methods=["GET", "POST"])
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
            db.session.add(AnswerGuess(guess=guess, answer=Answer.query.filter(db.and_(Answer.question.has(quiz=quiz), Answer.text == answers[i][int(answers_form[i])])).first()))
        db.session.commit()

        resp = make_response(redirect(url_for("quizanswers", id_=id_)))
        resp.set_cookie(id_, "guess.id_")
        return resp

    if request.cookies.get(id_):
        return redirect(url_for("quizanswers", id_=id_))
    else:
        return render_template("quiz.html", form=form, questions=[x.format(quiz.name) for x in questiontexts_name], answers=answers, id_=request.cookies.get("quiz"), name=quiz.name, title=f"Wie gut kennst du {quiz.name}?")


@app.route("/a/<id_>")
def quizanswers(id_):
    if not request.cookies.get(id_):
        return redirect(url_for("quiz", id_=id_))

    id_ = int(id_)
    quiz = Quiz.query.get(id_)
    if not quiz:
        return render_template("noquiz.html", id_=request.cookies.get("quiz"))
    page = request.args.get("page") or 1

    answers_quiz = quiz.guesses.all()
    answers_ordered = sorted(answers_quiz, key=lambda a: a.score(), reverse=True)
    answers_page = answers_ordered[Config.ANSWERS_PER_PAGE*(page-1):
                                   Config.ANSWERS_PER_PAGE*(page)]
    names = [answer.name for answer in answers_page]
    scores = [answer.score() for answer in answers_page]

    questions_corr, answers_corr = [], []

    for q in sorted(quiz.questions, key=lambda x: x.index):
        for a in q.answers:
            if a.correct_answer:
                questions_corr.append(q.text)
                answers_corr.append(a.text)

    if request.cookies.get("quiz") == id_:
        return render_template("quizanswers.html", answers=zip(names, scores),
                               correct_answers=zip(questions_corr, answers_corr, [None for i in range(len(answers_corr))]),
                               id_=request.cookies.get("quiz"), name=quiz.name,
                               max_score=len(questions))
    else:
        try:
            user_guess = Guess.query.get(int(request.cookies.get(str(id_))))
        except ValueError:
            user_guess = Guess.query.first()
        user_answers = []
        for answer in sorted(user_guess.answer_guesses, key=lambda x: x.answer.question.index):
            user_answers.append(answer.answer.text)
        return render_template("quizanswers.html", answers=zip(names, scores),
                               correct_answers=zip(questions_corr, answers_corr, user_answers),
                               id_=request.cookies.get("quiz"), name=quiz.name,
                               max_score=len(questions), id=id_)



@app.errorhandler(404)
def error_404(err):
    return render_template("err404.html", id_=request.cookies.get("quiz"))


@app.errorhandler(500)
def error_500(err):
    return render_template("err500.html", id_=request.cookies.get("quiz"))
