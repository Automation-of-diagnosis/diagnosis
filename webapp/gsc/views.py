from flask import Blueprint, request

from webapp.gsc import funcs as funcs_gsc

blueprint = Blueprint('gsc', __name__, url_prefix='/gsc')


@blueprint.route("/choice", methods=["GET", "POST"])
def choice():
    choice_user = request.form['index']
    if choice_user == 'New':
        return funcs_gsc.index()
    else:
        return funcs_gsc.add_data(int(choice_user))


@blueprint.route("/add_data", methods=["GET", "POST"])
def add_data():
    return funcs_gsc.update_db()
