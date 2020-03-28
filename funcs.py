import logging
from typing import Dict, Union, List, Optional

from flask import request, render_template, flash, redirect, url_for

from forms import LoginForm, choices_srad
from models import AppClass, RequestUser

logger = logging.getLogger('my_app')


def result_sofa(points_sofa):
    if points_sofa < 2:
        return f"Количество баллов {points_sofa}. Вероятность летального исхода: 0,0%"
    elif points_sofa < 4:
        return f"Количество баллов {points_sofa}. Вероятность летального исхода: 6,4%"
    elif points_sofa < 6:
        return f"Количество баллов {points_sofa}. Вероятность летального исхода: 20,2%"
    elif points_sofa < 8:
        return f"Количество баллов {points_sofa}. Вероятность летального исхода: 21,5%"
    elif points_sofa < 10:
        return f"Количество баллов {points_sofa}. Вероятность летального исхода: 33,3%"
    elif points_sofa < 12:
        return f"Количество баллов {points_sofa}. Вероятность летального исхода: 50,0%"
    return f"Количество баллов {points_sofa}. Вероятность летального исхода: 95,2%"


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
        print(1)
        row = RequestUser(full_name=ful_name,
                          age=age,
                          number=number,
                          srad=choices_srad[int(srad)],
                          creatinine=creatinine,
                          bilirubin=bilirubin,
                          platelets=platelets,
                          pao2_fio2=pao2_fio2,
                          gsc=gsc, )
        row.save()
        print(user_data)
        print(sofa(user_data))
        # return flash(result_sofa(sofa(user_data)))
    return render_template('index.html', page_title=title, scale=scale, form=form)


SOFA: Dict[str, Dict] = {'platelets': {'scale': [150, 100, 50, 20], 'direction': 'down'},
                        'pao2_fio2': {'scale': [400, 300, 200, 100], 'direction': 'down'},
                        'gsc': {'scale': [14, 12, 9, 6], 'direction': 'down'},
                        'creatinine': {'scale': [110, 171, 300, 440], 'direction': 'up'},
                        'bilirubin': {'scale': [20, 33, 102, 204], 'direction': 'up'},
                        }


def sofa_direction(measure: int, scale: list, direction: str) -> int:
    if direction == "up":
        scale = list(scale[::-1])
    for sofa_points, measure_border in enumerate(scale):
        if measure > measure_border:
            return 0 + sofa_points
    return 4


def sofa(user_data: Dict[str, int]) -> Union[int, str]:
    n = 0
    for measurement in user_data:
        try:
            user_data[measurement] = int(user_data[measurement])
        except TypeError:
            return 'Вводимые значения должны быть числа'
        if measurement == 'srad':
            n += user_data[measurement]
        elif measurement in SOFA:
            assesment = sofa_direction(user_data[measurement], SOFA[measurement]['scale'], SOFA[measurement]['direction'])
            n += assesment
    return n
