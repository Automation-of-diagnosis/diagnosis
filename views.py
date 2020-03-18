from my_app import app
import funcs


@app.route("/", methods=["POST"])
def index():
    return funcs.index()


# запуск функции при открытии страницы create
@app.route("/create", methods=["POST"])
def create_session():
    return funcs.create_session()


@app.route("/get_data", methods=["GET"])
def get_data_from_user():
    return funcs.get_data_from_user()


@app.route("/update_db", methods=["GET"])
def update_data_in_db():
    return funcs.update_data_in_db()
