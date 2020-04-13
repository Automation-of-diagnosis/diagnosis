import logging
import peewee
from typing import Dict, List, Union

from flask import flash, redirect, render_template, request, url_for

from webapp.gsc.forms import LoginForm, choices_srad,  AddDataForm
from webapp.gsc.models import RequestUser

logger = logging.getLogger('my_app')

BORDER_ANSWER = {2: 'Вероятность летального исхода: 0,0%',
                 4: 'Вероятность летального исхода: 6,4%',
                 6: 'Вероятность летального исхода: 20,2%',
                 8: 'Вероятность летального исхода: 21,5%',
                 10: 'Вероятность летального исхода: 33,3%',
                 12: 'Вероятность летального исхода: 50,0%',
                 }

RUSSIAN_MEANS = {'full_name': "Ф.И.О.",
                 'age': 'Возраст',
                 'srad': 'срАД',
                 'creatinine': 'Креатинин',
                 'platelets': 'Тромбоциты',
                 'bilirubin': 'Билирубин',
                 'pao2_fio2': 'PaO2/FiO2',
                 'gsc': 'GSC',
                 }


SOFA: Dict[str, Dict] = {'platelets': {'scale': [150, 100, 50, 20], 'direction': 'down'},
                         'pao2_fio2': {'scale': [400, 300, 200, 100], 'direction': 'down'},
                         'gsc': {'scale': [14, 12, 9, 6], 'direction': 'down'},
                         'creatinine': {'scale': [110, 171, 300, 440], 'direction': 'up'},
                         'bilirubin': {'scale': [20, 33, 102, 204], 'direction': 'up'},
                         }

CHECK_NULL_DATA_DICT = {'full_name': '',
                        'age': None,
                        'srad': 'None',
                        'creatinine': None,
                        'platelets': None,
                        'bilirubin': None,
                        'pao2_fio2': None,
                        'gsc': None}


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
                flash('Такой номер истории болезни уже существует')
                return redirect(url_for('index'))
    except peewee.DoesNotExist:
        return number_list_in_db


def list_with_null_data(number_list: int) -> List:
    data_from_db = dict_db(number_list)
    list_null = []
    for elem in data_from_db:
        if not data_from_db[elem] or data_from_db[elem] == "('0', '')":
            list_null.append(elem)
    return list_null


def dict_with_data_from_db(number_list: int) -> Dict:
    data_from_db = dict_db(int(number_list))
    data_from_db['srad'] = data_from_db['srad'][2]
    del(data_from_db['full_name'])
    del(data_from_db['age'])
    return data_from_db


def check_and_print_result(check_list: list, number_list: int, user_data: Dict[str, int]):
    if len(check_list) > 0:
        flash('Ваши данные сохранены для расчёта')
        flash(f'Для истории болезни №{number_list} необходимо будет добавить следующие данные:')
        for element in check_list:
            flash(f'{element}')
        return redirect(url_for('index'))
    else:
        flash(result_sofa(sofa(user_data), BORDER_ANSWER))
        return redirect(url_for('index'))


def update_db():
    number = request.form['index']
    form = AddDataForm()
    full_name = form.full_name.data
    age = form.age.data
    srad = form.srad.data
    creatinine = form.creatinine.data
    platelets = form.platelets.data
    bilirubin = form.bilirubin.data
    pao2_fio2 = form.pao2_fio2.data
    gsc = form.gsc.data
    user_data_update = {
        'full_name': full_name,
        'age': age,
        'srad': srad,
        'creatinine': creatinine,
        'platelets': platelets,
        'bilirubin': bilirubin,
        'pao2_fio2': pao2_fio2,
        'gsc': gsc,
    }
    if user_data_update == CHECK_NULL_DATA_DICT:
        flash('Вы ничего не ввели, начните сначало')
        return index()

    for data_user in user_data_update:
        if user_data_update[data_user] or (data_user == 'srad' and user_data_update[data_user] != 'None'):
            if data_user == 'full_name':
                RequestUser.update(full_name=user_data_update[data_user]).where(RequestUser.number == number).execute()
            if data_user == 'age':
                RequestUser.update(age=user_data_update[data_user]).where(RequestUser.number == number).execute()
            if data_user == 'srad' and user_data_update[data_user] != 'None':
                RequestUser.update(srad=choices_srad[int(user_data_update[data_user])]).\
                    where(RequestUser.number == number).execute()
            if data_user == 'creatinine':
                RequestUser.update(creatinine=user_data_update[data_user]).where(RequestUser.number == number).execute()
            if data_user == 'platelets':
                RequestUser.update(platelets=user_data_update[data_user]).where(RequestUser.number == number).execute()
            if data_user == 'bilirubin':
                RequestUser.update(bilirubin=user_data_update[data_user]).where(RequestUser.number == number).execute()
            if data_user == 'pao2_fio2':
                RequestUser.update(pao2_fio2=user_data_update[data_user]).where(RequestUser.number == number).execute()
            if data_user == 'gsc':
                RequestUser.update(gsc=user_data_update[data_user]).where(RequestUser.number == number).execute()
    flash('Ваши данные добавлены')
    list_null = list_with_null_data(int(number))
    if len(list_null) == 0:
        flash('Все данные заполнены')
        # flash('Чтобы узнать результат просто введите ещё раз номер больничного листа в расчёт')
        flash(result_sofa(sofa(dict_with_data_from_db(number)), BORDER_ANSWER))
        dict_with_data_from_db(number)
    return index()


def add_data(number: int):
    form = AddDataForm()
    title = 'Оценка тяжести состояния пациента'
    scale = 'Введите показатели:'
    adddata = RequestUser.get(RequestUser.number == number)
    return render_template('add_data.html', adddata=adddata, page_title=title, scale=scale, form=form, number=number)


def index():
    form = LoginForm()
    title = 'Оценка тяжести состояния пациента'
    scale = 'Введите показатели:'
    # gsc = request.form['gsc'] #другой способ для доступа к элементу данных полученных от пользователя
    # print(gsc)
    number = form.number.data
    if number:
        full_name = form.full_name.data
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
            row = RequestUser(full_name=full_name,
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
                if not user_data[data] or (data == 'srad' and user_data[data] == '0'):
                    list_add.append(RUSSIAN_MEANS[data])
            check_and_print_result(list_add, number, user_data)
        else:
            list_null = list_with_null_data(number)
            if len(list_null) == 0:
                flash('Все данные были заполнены ранее и выполнен расчёт')
                flash(result_sofa(sofa(dict_with_data_from_db(number)), BORDER_ANSWER))
                return redirect(url_for('index'))

            flash('Необходимо дозаполнить следующие данные:')
            for elem in list_null:
                flash(f'{RUSSIAN_MEANS[elem]}')
            return render_template('choice.html', number=number)
    return render_template('index.html', page_title=title, scale=scale, form=form)


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


# Функция получает данные из базы данных по номеру истории болезни
def dict_db(number_list: int) -> Dict[str, Union[str, int]]:
    data_from_db = {}
    for data in RequestUser.select():
        if data.number == number_list:
            data_from_db['full_name'] = data.full_name
            data_from_db['age'] = data.age
            data_from_db['srad'] = data.srad
            data_from_db['creatinine'] = data.creatinine
            data_from_db['bilirubin'] = data.bilirubin
            data_from_db['platelets'] = data.platelets
            data_from_db['pao2_fio2'] = data.pao2_fio2
            data_from_db['gsc'] = data.gsc
    return data_from_db
