import logging

from flask import request

from models import App_class

logger = logging.getLogger('my_app')


# Уточнить как можно получить проверку данных
def check_data_on_validation():
    if "user_data" not in request.headers:
        raise Exception("Invalid request")


def func1_create_session():
    try:
        logger.debug("Session started")
        check_data_on_validation()
        return {"data": "Result session...", "error": "Ok"}
    except Exception as ex:
        logger.warning(ex)
        return {"data": None, "error": str(ex)}
    finally:
        logger.debug("Session finished")


def func2_get_data_from_user():
    try:
        logger.debug("Get data started")
        check_data_on_validation()
        # TODO and filter
        data_user = App_class.select()
        return {"data": [p.to_dict() for p in data_user], "error": "Ok"}
    except Exception as ex:
        logger.warning(ex)
        return {"data": None, "error": str(ex)}
    finally:
        logger.debug("Get data finished")


def update_data_in_db():
    try:
        logger.debug("Update db started")
        check_data_on_validation()
        # TODO and check form params
        data_user_in_db = App_class.create(**request.form)
        return {"data": data_user_in_db.to_dict(), "error": "Ok"}
    except Exception as ex:
        logger.warning(ex)
        return {"data": None, "error": str(ex)}
    finally:
        logger.debug("Update db finished")
