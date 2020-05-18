import logging
import peewee
from typing import Dict, List, Union

from flask import flash, redirect, render_template, request, url_for

from webapp.gsc.forms import LoginForm, choices_srad,  AddDataForm, choices_eye_response, \
    choices_motor_response, choices_verbal_response
from webapp.gsc.models import RequestUser

logger = logging.getLogger('my_app')

GSC_ANSWER = {3: 'смерть мозга терминальная кома',
                 8: 'кома',
                 12: 'сопор',
                 14: 'оглушение',
                 15: 'ясное сознание',
              }

BORDER_ANSWER = {2: 'вероятность летального исхода: 0,0%',
                 4: 'вероятность летального исхода: 6,4%',
                 6: 'вероятность летального исхода: 20,2%',
                 8: 'вероятность летального исхода: 21,5%',
                 10: 'вероятность летального исхода: 33,3%',
                 12: 'вероятность летального исхода: 50,0%',
                 }


RUSSIAN_MEANS = {'full_name': "Ф.И.О.",
                 'age': 'Возраст',
                 'srad': 'срАД',
                 'creatinine': 'Креатинин',
                 'platelets': 'Тромбоциты',
                 'bilirubin': 'Билирубин',
                 'pao2_fio2': 'PaO2/FiO2',
                 'eye_response': 'Открывание глаз',
                 'verbal_response': 'Словесный ответ',
                 'motor_response': 'Двигательная реакция',
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
                        'eye_response': 'None',
                        'verbal_response': 'None',
                        'motor_response': 'None',
                        }


def index():
    """Main function that controls data acquisition and output"""
    form = LoginForm()
    title = 'Оценка тяжести состояния пациента'
    scale = 'Введите показатели:'
    # gsc = request.form['gsc'] #другой способ для доступа к элементу данных полученных от пользователя
    # print(gsc)
    number = form.number.data
    # if form.validate_on_submit():
    #     pass
    # else:
    #     for field, errors in form.errors.items():
    #         for error in errors:
    #             flash('Ошибка в заполнении поля "{}": - {}'.format(getattr(form, field).label.text, error))
    if number:
        full_name = form.full_name.data
        age = form.age.data
        srad = form.srad.data
        creatinine = form.creatinine.data
        platelets = form.platelets.data
        bilirubin = form.bilirubin.data
        pao2_fio2 = form.pao2_fio2.data
        eye_response = form.eye_response.data
        verbal_response = form.verbal_response.data
        motor_response = form.motor_response.data
        user_data = {
            'srad': srad,
            'creatinine': creatinine,
            'platelets': platelets,
            'bilirubin': bilirubin,
            'pao2_fio2': pao2_fio2,
            'eye_response': eye_response,
            'verbal_response': verbal_response,
            'motor_response': motor_response,
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
                              eye_response=choices_eye_response[int(eye_response)],
                              verbal_response=choices_verbal_response[int(verbal_response)],
                              motor_response=choices_motor_response[int(motor_response)],
                              )
            row.save()
            list_add = []
            for data in user_data:
                if not user_data[data] or (data == 'srad' and user_data[data] == '0')\
                        or (data == 'eye_response' and user_data[data] == '0')\
                        or (data == 'verbal_response' and user_data[data] == '0')\
                        or (data == 'motor_response' and user_data[data] == '0'):
                    list_add.append(RUSSIAN_MEANS[data])
            check_and_print_result(list_add, number, user_data)
        else:
            list_null = list_with_null_data(number)
            if len(list_null) == 0:
                flash('Все данные были заполнены ранее и выполнен расчёт')
                save_result_in_db(number)
                return redirect(url_for('index'))

            flash('Необходимо дозаполнить следующие данные:')
            for elem in list_null:
                flash(f'{RUSSIAN_MEANS[elem]}')
            return render_template('gsc/choice.html', number=number)
    return render_template('gsc/index.html', page_title=title, scale=scale, form=form)


def result_gsc(points_sofa: List[int], border: Dict[int, str]) -> str:
    """Function create answer GSC by the number of points
    >>> result_gsc([0,5], GSC_ANSWER)
    'GSC - 5 баллов (кома)'
    >>> result_gsc([0,2], GSC_ANSWER)
    'GSC - 2 балла (смерть мозга терминальная кома)'
    >>> result_gsc([0,1], GSC_ANSWER)
    'GSC - 1 балл (смерть мозга терминальная кома)'
    >>> result_gsc([0,4], GSC_ANSWER)
    'GSC - 4 балла (кома)'
    >>> result_gsc([0,12], GSC_ANSWER)
    'GSC - 12 баллов (сопор)'
    >>> result_gsc([0,17], GSC_ANSWER) is None
    True
    >>> result_gsc([0,0], GSC_ANSWER)
    'GSC - 0 баллов (смерть мозга терминальная кома)'
    """
    for answer in border:
        if points_sofa[1] <= answer:
            if points_sofa[1] == 1:
                word_point = 'балл'
            elif 1 < points_sofa[1] <= 4:
                word_point = 'балла'
            else:
                word_point = 'баллов'
            return f'GSC - {points_sofa[1]} {word_point} ({border[answer]})'


def result_sofa(points_sofa: List[int], border: Dict[int, str]) -> str:
    """Function  create answer SOFA by the number of points
    >>> result_sofa([4,14], BORDER_ANSWER)
    'Sofa - 5 баллов, вероятность летального исхода: 20,2%'
    >>> result_sofa([1,14], BORDER_ANSWER)
    'Sofa - 2 балла, вероятность летального исхода: 6,4%'
    >>> result_sofa([0,14], BORDER_ANSWER)
    'Sofa - 1 балл, вероятность летального исхода: 0,0%'
    >>> result_sofa([3,14], BORDER_ANSWER)
    'Sofa - 4 балла, вероятность летального исхода: 20,2%'
    >>> result_sofa([8,5], BORDER_ANSWER)
    'Sofa - 12 баллов, вероятность летального исхода: 95,2%'
    >>> result_sofa([7,5], BORDER_ANSWER)
    'Sofa - 11 баллов, вероятность летального исхода: 50,0%'
    >>> result_sofa([12,0], BORDER_ANSWER)
    'Sofa - 16 баллов, вероятность летального исхода: 95,2%'
    """
    n, gsc = points_sofa
    if gsc < 6:
        n += 4
    elif gsc < 10:
        n += 3
    elif gsc < 13:
        n += 2
    elif gsc < 15:
        n += 1
    if n > 11:
        return f'Sofa - {n} баллов, вероятность летального исхода: 95,2%'
    for answer in border:
        if n < answer:
            if n == 1:
                word_point = 'балл'
            elif 1 < n <= 4:
                word_point = 'балла'
            else:
                word_point = 'баллов'
            return f'Sofa - {n} {word_point}, {border[answer]}'


def check_number_list_in_db(number_list: int) -> bool:
    """Function checks for sick leave in db"""
    number_list_in_db = False
    try:
        for data in RequestUser.select():
            if data.number == number_list:
                flash('Такой номер истории болезни уже существует')
                return redirect(url_for('index'))
    except peewee.DoesNotExist:
        return number_list_in_db


def list_with_null_data(number_list: int) -> List:
    """Function checks Null data in db"""
    data_from_db = dict_db(number_list)
    list_null = []
    for elem in data_from_db:
        if not data_from_db[elem] or data_from_db[elem] == "('0', '')":
            list_null.append(elem)
    return list_null


def dict_with_data_from_db(number_list: int) -> Dict:
    """Function gets data from db"""
    data_from_db = dict_db(int(number_list))
    data_from_db['srad'] = data_from_db['srad'][2]
    data_from_db['eye_response'] = data_from_db['eye_response'][2]
    data_from_db['verbal_response'] = data_from_db['verbal_response'][2]
    data_from_db['motor_response'] = data_from_db['motor_response'][2]
    del(data_from_db['full_name'])
    del(data_from_db['age'])
    return data_from_db


def check_and_print_result(check_list: list, number_list: int, user_data: Dict[str, int]):
    """Function gets and shows fields with Null or print result if all fields not Null"""
    if len(check_list) > 0:
        flash('Ваши данные сохранены для расчёта')
        flash(f'Для истории болезни №{number_list} необходимо будет добавить следующие данные:')
        for element in check_list:
            flash(f'{element}')
        return redirect(url_for('index'))
    else:
        answer_sofa = result_sofa(sofa(user_data), BORDER_ANSWER)
        answer_gsc = result_gsc(sofa(user_data), GSC_ANSWER)
        RequestUser.update(result_sofa=answer_sofa).where(RequestUser.number == number_list).execute()
        RequestUser.update(result_gsc=answer_gsc).where(RequestUser.number == number_list).execute()
        flash('Все данные были заполнены, результаты расчёта следующие:')
        flash(answer_sofa)
        flash(answer_gsc)
        return redirect(url_for('index'))


def change_data_in_db(user_data_update, number):
    """Function record data in db when replenish"""
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
            if data_user == 'eye_response' and user_data_update[data_user] != 'None':
                RequestUser.update(eye_response=choices_eye_response[int(user_data_update[data_user])]).\
                    where(RequestUser.number == number).execute()
            if data_user == 'verbal_response' and user_data_update[data_user] != 'None':
                RequestUser.update(verbal_response=choices_verbal_response[int(user_data_update[data_user])]).\
                    where(RequestUser.number == number).execute()
            if data_user == 'motor_response' and user_data_update[data_user] != 'None':
                RequestUser.update(motor_response=choices_motor_response[int(user_data_update[data_user])]).\
                    where(RequestUser.number == number).execute()


def save_result_in_db(number):
    """Function save result in db"""
    if not RequestUser.get(RequestUser.number == number).result_sofa:
        answer_sofa = result_sofa(sofa(dict_with_data_from_db(number)), BORDER_ANSWER)
        answer_gsc = result_gsc(sofa(dict_with_data_from_db(number)), GSC_ANSWER)
        RequestUser.update(result_sofa=answer_sofa).where(RequestUser.number == number).execute()
        RequestUser.update(result_gsc=answer_gsc).where(RequestUser.number == number).execute()
        flash('Результаты расчёта следующие:')
        flash(answer_sofa)
        flash(answer_gsc)
    else:
        flash('Результаты расчёта следующие:')
        flash(RequestUser.get(RequestUser.number == number).result_sofa)
        flash(RequestUser.get(RequestUser.number == number).result_gsc)


def update_db():
    """Function save result in db"""
    number = request.form['index']
    form = AddDataForm()
    full_name = form.full_name.data
    age = form.age.data
    srad = form.srad.data
    creatinine = form.creatinine.data
    platelets = form.platelets.data
    bilirubin = form.bilirubin.data
    pao2_fio2 = form.pao2_fio2.data
    eye_response = form.eye_response.data
    verbal_response = form.verbal_response.data
    motor_response = form.motor_response.data
    user_data_update = {
        'full_name': full_name,
        'age': age,
        'srad': srad,
        'creatinine': creatinine,
        'platelets': platelets,
        'bilirubin': bilirubin,
        'pao2_fio2': pao2_fio2,
        'eye_response': eye_response,
        'verbal_response': verbal_response,
        'motor_response': motor_response,
    }
    if user_data_update == CHECK_NULL_DATA_DICT:
        flash('Вы ничего не ввели, начните сначало')
        return index()

    change_data_in_db(user_data_update, number)
    flash('Ваши данные добавлены')
    list_null = list_with_null_data(int(number))
    if len(list_null) == 0:
        flash('Все данные заполнены')
        save_result_in_db(number)
    return index()


def add_data(number: int):
    """Function shows a page with indicators that are not enough to calculate"""
    form = AddDataForm()
    title = 'Оценка тяжести состояния пациента'
    scale = 'Введите показатели:'
    addata = RequestUser.get(RequestUser.number == number)
    return render_template('gsc/add_data.html', adddata=addata, page_title=title, scale=scale, form=form, number=number)


def sofa_direction(measure: int, scale: list, direction: str) -> int:
    """Function that counts points for SOFA"""
    if direction == "up":
        scale = list(scale[::-1])
    for sofa_points, measure_border in enumerate(scale):
        if measure > measure_border:
            return 0 + sofa_points
    return 4


def sofa(user_data: Dict[str, int]) -> Union[str, List[int]]:
    """Function that counts the total points SOFA and in particular GSC"""
    n = 0
    gsc = 0
    for measurement in user_data:
        try:
            user_data[measurement] = int(user_data[measurement])
        except TypeError:
            return 'Вводимые значения должны быть числа'
        if measurement == 'eye_response' or measurement == 'verbal_response' or measurement == 'motor_response':
            gsc += user_data[measurement]
        elif measurement == 'srad':
            n += user_data[measurement]
        elif measurement in SOFA:
            assesment = sofa_direction(user_data[measurement], SOFA[measurement]['scale'],
                                       SOFA[measurement]['direction'])
            n += assesment
    return [n, gsc]


# Функция получает данные из базы данных по номеру истории болезни
def dict_db(number_list: int) -> Dict[str, Union[str, int]]:
    """Function take data from db and return dict with data"""
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
            data_from_db['eye_response'] = data.eye_response
            data_from_db['verbal_response'] = data.verbal_response
            data_from_db['motor_response'] = data.motor_response
    return data_from_db


if __name__ == "__main__":
    import doctest
    doctest.testmod()
