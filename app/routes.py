from random import randint

from flask import (flash, make_response, redirect, render_template, request,
                   url_for)

from app import app, db
from app.forms import QuizForm
from app.models import Answer, Quiz
from app.quiz import answers, questions
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
            if Quiz.get(request.cookies.get("quiz")):
                flash("Quiz geändert!")
                Quiz.get(request.cookies.get("quiz")).name = name
                Quiz.get(request.cookies.get("quiz")).correct_answers = " ".join(answers_form)
                redirect(url_for("index"))
        else:
            # 64 ** 10 - 1
            id_ = randint(0, 10**10 - 1)

            # new quiz entry
            quiz = Quiz(id_=id_, name=name, correct_answers=" ".join(answers_form))
            db.session.add(quiz)
            db.session.commit()

            # quiz id as base64
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie("quiz", str(id_))
            resp.set_cookie(str(id_), "True")

            return resp

    return render_template("newquiz.html", form=form,
                           questions=questions,
                           answers=answers, id_=request.cookies.get("quiz"))


@app.route("/quiz/<id_>", methods=["GET", "POST"])
def quiz(id_):
    if not Quiz.query.get(id_):
        return render_template("noquiz.html")
    form = QuizForm()
    fields = list(form.__dict__.values())[7:-1]

    if form.validate_on_submit():
        flash("Quiz abgeschickt!")
        name = form.name.data
        answers_form = form.answers.data.split()

        answer = Answer(name=name, answers=" ".join(answers_form),
                        quiz=Quiz.query.get(id_))
        db.session.add(answer)
        db.session.commit()

        resp = make_response(redirect(url_for("quizanswers", id_=id_)))
        resp.set_cookie(id_, "True")
        return resp

    if request.cookies.get(id_):
        return redirect(url_for("quizanswers", id_=id_))
    else:
        return render_template("quiz.html", form=form, fields=fields, id_=request.cookies.get("quiz"))


@app.route("/quizanswers/<id_>")
def quizanswers(id_):
    if not request.cookies.get(id_):
        return redirect(url_for("quiz", id_=id_))

    id_b10 = int(id_)
    quiz = Quiz.query.get(id_b10)
    if not quiz:
        return render_template("noquiz.html",)
    page = request.args.get("page") or 1
    answers_quiz = quiz.answers.all()
    answers_ordered = sorted(answers_quiz, key=lambda a: a.score())
    answers_page = answers_ordered[Config.ANSWERS_PER_PAGE*(page-1):
                                   Config.ANSWERS_PER_PAGE*(page)]
    names = [answer.name for answer in answers_page]
    scores = [answer.score() for answer in answers_page]

    correct_answers = quiz.correct_answers.split()

    correct_answers = [answer[int(correct_answer)] for answer, correct_answer in zip(answers, correct_answers)]
    return render_template("quizanswers.html", answers=zip(names, scores),
                           correct_answers=zip(questions, correct_answers), id_=request.cookies.get("quiz"))
