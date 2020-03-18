import logging
from typing import Dict, Union

from flask import request, render_template

from forms import LoginForm
from models import AppClass

logger = logging.getLogger('my_app')


def index():
    try:

        title = 'Оценка тяжести состояния пациента'
        scale = 'Введите показатели:'
        return render_template('index.html', page_title=title, scale=scale)
    except (IndexError, TypeError):
        return False

SOFA_down: Dict[str, str] = {'platelets': '150 100 50 20',
                        'PaO2/FiO2': '400 300 200 100',
                        'gsc': '14 12 9 6',
                             }

SOFA_up: Dict[str, str] = {'creatinine': '110 171 300 440',
                           'bilirubin': '20 33 102 204',
                           }

user_data: Dict[str, str] = {'srAD': '4',
                        'creatinine': '150',
                        'bilirubin': '16',
                             'platelets': '25',
                             'PaO2/FiO2': '150',
                             'gsc': '3',
                             }


def sofa_down(measure: int, scale: str) -> int:
    list_scale = scale.split()
    if measure < int(list_scale[3]):
        return 4
    elif measure < int(list_scale[2]):
        return 3
    elif measure < int(list_scale[1]):
        return 2
    elif measure < int(list_scale[0]):
        return 1
    else:
        return 0


def sofa_up(measure: int, scale: str) -> int:
    list_scale = scale.split()
    if measure < int(list_scale[0]):
        return 0
    elif measure < int(list_scale[1]):
        return 1
    elif measure < int(list_scale[2]):
        return 2
    elif measure < int(list_scale[3]):
        return 3
    else:
        return 4


def sofa(user_data: Dict[str, str]) -> Union[int, str]:
    n = 0
    for measurement in user_data:
        try:
            user_data[measurement] = int(user_data[measurement])
        except TypeError:
            return 'Вводимые значения должны быть числа'
        if measurement == 'srAD':
            if user_data[measurement] > 70:
                n += 1
        if measurement in SOFA_down:
            assesment = sofa_down(user_data[measurement], SOFA_down[measurement])
            n += assesment
        else:
            assesment = sofa_up(user_data[measurement], SOFA_up[measurement])
            n += assesment
    return n


# Уточнить как можно получить проверку данных
def check_data_on_validation():
    if "user_data" not in request.headers:
        raise Exception("Invalid request")


def create_session() -> Dict[str, Union[str, None]]:
    try:
        logger.debug("Session started")
        check_data_on_validation()
        return {"data": "Result session...", "error": "Ok"}
    except Exception as ex:
        logger.warning(ex)
        return {"data": None, "error": str(ex)}
    finally:
        logger.debug("Session finished")


def get_data_from_user() -> Dict[str, Union[str, None]]:
    try:
        logger.debug("Get data started")
        check_data_on_validation()
        # TODO and filter
        data_user = AppClass.select()
        return {"data": [p.to_dict() for p in data_user], "error": "Ok"}
    except Exception as ex:
        logger.warning(ex)
        return {"data": None, "error": str(ex)}
    finally:
        logger.debug("Get data finished")


def update_data_in_db() -> Dict[str, Union[str, None]]:
    try:
        logger.debug("Update db started")
        check_data_on_validation()
        # TODO and check form params
        data_user_in_db = AppClass.create(**request.form)
        return {"data": data_user_in_db.to_dict(), "error": "Ok"}
    except Exception as ex:
        logger.warning(ex)
        return {"data": None, "error": str(ex)}
    finally:
        logger.debug("Update db finished")
