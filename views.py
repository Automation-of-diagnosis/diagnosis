from typing import Dict, Union

from my_app import app
import funcs


# запуск функции при открытии страницы create
@app.route("/create", methods=["POST"])
def func1_create_session() -> Dict[Union[str, None], str]:
    return funcs.func1_create_session()


@app.route("/get_data", methods=["GET"])
def func2_get_data_from_user() -> Dict[Union[str, None], str]:
    return funcs.func2_get_data_from_user()


@app.route("/update_db", methods=["GET"])
def update_data_in_db() -> Dict[Union[str, None], str]:
    return funcs.update_data_in_db()
