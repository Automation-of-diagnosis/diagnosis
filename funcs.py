import logging
from typing import Dict, Union, Optional

from flask import request, render_template, flash, redirect, url_for

from forms import LoginForm
from models import AppClass, RequestUser

logger = logging.getLogger('my_app')


def index():
    form = LoginForm()
    # form.srad.data = '0' # выбор поля по умолчанию
    title = 'Оценка тяжести состояния пациента'
    scale = 'Введите показатели:'
    # gsc = request.form['gsc'] #другой способ для доступа к элементу данных полученных от пользователя
    # print(gsc)
    if form.validate_on_submit(): # если все поля формы были заполнены то выполнить
        ful_name = form.ful_name.data
        age = form.age.data
        number = form.number.data
        srad = form.srad.data
        creatinine = form.creatinine.data
        platelets = form.platelets.data
        bilirubin = form.bilirubin.data
        pao2_fio2 = form.pao2_fio2.data
        gsc = form.gsc.data
        user_data = {
            'srad': srad,
            'creatinine': creatinine,
            'platelets': platelets,
            'bilirubin': bilirubin,
            'pao2_fio2': pao2_fio2,
            'gsc': gsc,
        }
        print(user_data)
        print(sofa(user_data))
        # return flash("Выполняется подсчёт")
    return render_template('index.html', page_title=title, scale=scale, form=form)


SOFA_down: Dict[str, str] = {'platelets': '150 100 50 20',
                        'pao2_fio2': '400 300 200 100',
                        'gsc': '14 12 9 6',
                             }

SOFA_up: Dict[str, str] = {'creatinine': '110 171 300 440',
                           'bilirubin': '20 33 102 204',
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
        if measurement == 'srad':
            n += user_data[measurement]
        elif measurement in SOFA_down:
            assesment = sofa_down(user_data[measurement], SOFA_down[measurement])
            n += assesment
        elif measurement in SOFA_up:
            assesment = sofa_up(user_data[measurement], SOFA_up[measurement])
            n += assesment
    return n
