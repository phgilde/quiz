# Installation
To install this flask app on your system, simply run the following:
```
git clone https://github.com/phgilde/quiz.git
py -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
flask db upgrade
```
To run the app on your system, simply run the following (on Windows):
```
venv/Scripts/activate
set FLASK_APP=main.py
flask run
```
On linux, replace `set` with `export` and `Scripts` with `bin`.