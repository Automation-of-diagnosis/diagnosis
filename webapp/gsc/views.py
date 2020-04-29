from flask import Blueprint, request, json

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


# @blueprint.route("/api", methods=["GET", "POST", "PUT"])
# def api():
#     if request.method == 'GET':
#         return funcs_gsc.api_get(request.args.get('bol_list'))
#     if request.method == 'POST':
#         data = json.loads(request.data)
#         return funcs_gsc.api_post(data)
#     if request.method == 'PUT':
#         # return funcs_gsc.api_put(request.args.get('bol_list'))
#         pass
