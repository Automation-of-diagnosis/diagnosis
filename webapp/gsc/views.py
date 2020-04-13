from flask import request
from webapp.my_app import app
import funcs


@app.route("/", methods=["GET", "POST"])
def index():
    return funcs.index()


@app.route("/choice", methods=["GET", "POST"])
def choice():
    choice_user = request.form['index']
    if choice_user == 'New':
        return funcs.index()
    else:
        return funcs.add_data(int(choice_user))


@app.route("/add_data", methods=["GET", "POST"])
def add_data():
    return funcs.update_db()
