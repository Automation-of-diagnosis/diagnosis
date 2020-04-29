from flask import Blueprint, request, json

from webapp.api.funcs import api_get, api_post, api_put

blueprint = Blueprint('api', __name__)


@blueprint.route("/api", methods=["GET", "POST", "PUT"])
def api():
    if request.method == 'GET':
        return api_get(request.args.get('bol_list'))
    if request.method == 'POST':
        data = json.loads(request.data)
        return api_post(data)
    if request.method == 'PUT':
        data = json.loads(request.data)
        return api_put(data)
