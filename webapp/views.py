from flask import request

from webapp import gsc as funcs_gsc


# @app.route("/", methods=["GET", "POST"])
# def index():
#     return funcs_gsc.index()


@app.route("/choice", methods=["GET", "POST"])
def choice():
    choice_user = request.form['index']
    if choice_user == 'New':
        return funcs_gsc.index()
    else:
        return funcs_gsc.add_data(int(choice_user))


@app.route("/add_data", methods=["GET", "POST"])
def add_data():
    return funcs_gsc.update_db()
