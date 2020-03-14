from my_app import app
import funcs


# запуск функции при открытии страницы create
@app.route("/create", methods=["POST"])
def func1_create_session():
    return funcs.func1_create_session()


@app.route("/get_data", methods=["GET"])
def func2_get_data_from_user():
    return funcs.func2_get_data_from_user()


@app.route("/update_db", methods=["GET"])
def update_data_in_db():
    return funcs.update_data_in_db()
