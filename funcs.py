import logging
import peewee
from typing import Dict, Union

from flask import flash, redirect, render_template, request, url_for

from forms import LoginForm, choices_srad, ChoiceForm
from models import RequestUser

logger = logging.getLogger('my_app')

BORDER_ANSWER = {2: 'Вероятность летального исхода: 0,0%',
                 4: 'Вероятность летального исхода: 6,4%',
                 6: 'Вероятность летального исхода: 20,2%',
                 8: 'Вероятность летального исхода: 21,5%',
                 10: 'Вероятность летального исхода: 33,3%',
                 12: 'Вероятность летального исхода: 50,0%',
                 }

RUSSIAN_MEANS = {'srad': 'срАД',
                 'creatinine': 'Креатинин',
                 'platelets': 'Тромбоциты',
                 'bilirubin': 'Билирубин',
                 'pao2_fio2': 'PaO2/FiO2',
                 'gsc': 'GSC',
                 }


def result_sofa(points_sofa: int, border: Dict[int, str]) -> str:
    if points_sofa > 11:
        return f'Количество баллов {points_sofa}. Вероятность летального исхода: 95,2%'
    for answer in border:
        if points_sofa < answer:
            return f'Количество баллов {points_sofa}. {border[answer]}'


def check_number_list_in_db(number_list: int) -> bool:
    number_list_in_db = False
    try:
        for data in RequestUser.select():
            if data.number == number_list:
                flash('Такой больничный лист уже существует')
                return redirect(url_for('index'))
    except peewee.DoesNotExist:
        return number_list_in_db


def choice():
    form = ChoiceForm()
    return render_template('choice.html', form=form)


def index():
    form = LoginForm()
    title = 'Оценка тяжести состояния пациента'
    scale = 'Введите показатели:'
    # gsc = request.form['gsc'] #другой способ для доступа к элементу данных полученных от пользователя
    # print(gsc)
    number = form.number.data
    if number:
        ful_name = form.ful_name.data
        age = form.age.data
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
        number_list = check_number_list_in_db(number)
        if not number_list:
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
            list_add = []
            for data in user_data:
                if data == 'srad' and user_data[data] == '0':
                    list_add.append(RUSSIAN_MEANS[data])
                if user_data[data] == None:
                    list_add.append(RUSSIAN_MEANS[data])
            if len(list_add) > 0:
                flash('Ваши данные сохранены для расчёта')
                flash(f'Для больничного листа №{number} необходимо будет добавить следующие данные:')
                for element in list_add:
                    flash(f'{element}')
            else:
                flash(result_sofa(sofa(user_data), BORDER_ANSWER))
                # return redirect(url_for('index'))
        else:
            data_from_db = {}
            for data in RequestUser.select():
                if data.number == number:
                    data_from_db['srad'] = data.srad
                    data_from_db['creatinine'] = data.creatinine
                    data_from_db['bilirubin'] = data.bilirubin
                    data_from_db['platelets'] = data.platelets
                    data_from_db['pao2_fio2'] = data.pao2_fio2
                    data_from_db['gsc'] = data.gsc
            list_null = []
            for elem in data_from_db:
                if data_from_db[elem] == "('0', '')":
                    list_null.append(elem)
                if data_from_db[elem] == None:
                    list_null.append(elem)
            if len(list_null) == 0:
                flash('Все данные были заполнены и выполнен расчёт')
                return redirect(url_for('index'))

            flash('Необходимо дозаполнить следующие данные:')
            for elem in list_null:
                flash(f'{RUSSIAN_MEANS[elem]}')
            return choice()
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
            assesment = sofa_direction(user_data[measurement], SOFA[measurement]['scale'],
                                       SOFA[measurement]['direction'])
            n += assesment
    return n
