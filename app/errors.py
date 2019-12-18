from app import app
from flask import render_template, request


@app.errorhandler(404)
def error_404(err):
    return render_template("err404.html", id_=request.cookies.get("quiz"))


@app.errorhandler(500)
def error_500(err):
    return render_template("err500.html", id_=request.cookies.get("quiz"))
