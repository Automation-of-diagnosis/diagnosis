from webapp.gsc.forms import choices_srad, choices_eye_response, \
    choices_motor_response, choices_verbal_response
from webapp.gsc.models import RequestUser
from webapp.gsc.funcs import BORDER_ANSWER, change_data_in_db, check_number_list_in_db, dict_db, \
    dict_with_data_from_db, GSC_ANSWER, list_with_null_data, result_gsc, result_sofa, sofa

NAME_OF_INDICATORS = ('age', 'bilirubin', 'creatinine', 'eye_response', 'full_name', 'motor_response', 'pao2_fio2',
                      'platelets', 'srad', 'verbal_response')


def api_get(bol_list):
    int_bol_list = int(bol_list)
    number_list = check_number_list_in_db(int_bol_list)
    if not number_list:
        return "Такого больничного листа не существует. Используйте метод 'POST' чтобы создать его"
    answer = dict_db(int_bol_list)
    list_null = list_with_null_data(int_bol_list)
    if not list_null:
        res_gsi = result_sofa(sofa(dict_with_data_from_db(bol_list)), BORDER_ANSWER)
        res_sofa = result_gsc(sofa(dict_with_data_from_db(bol_list)), GSC_ANSWER)
        return {'data_from_db': answer, 'result_gsi': res_gsi, 'result_sofa': res_sofa, }
    return {'Для расчёта необходимо заполнить': list_null, 'data_from_db': answer}


def api_post(data):
    number = int(data['number'])
    number_list = check_number_list_in_db(number)
    if not number_list:
        for indicators in NAME_OF_INDICATORS:
            if indicators not in data:
                if indicators == 'srad' or indicators == 'eye_response' or indicators == 'verbal_response' \
                 or indicators == 'motor_response':
                    data[indicators] = 0
                else:
                    data[indicators] = None
        save_in_db(data)
        return {'Ваши данные приняты для расчёта': dict_db(int(number))}
    return f'Больничный лист с номером {number} существует. Для просмотра или измения данных - GET/PUT'


def api_put(data):
    number = int(data['number'])
    number_list = check_number_list_in_db(number)
    if not number_list:
        return "Такого больничного листа не существует. Используйте метод 'POST' чтобы создать его"
    change_data_in_db(data, number)
    return {'Ваши данные внесены в базу данных': dict_db(int(number))}


def save_in_db(data):
    srad = choices_srad[int(data['srad'])]
    eye_response = choices_eye_response[int(data['eye_response'])]
    verbal_response = choices_verbal_response[int(data['verbal_response'])]
    motor_response = choices_motor_response[int(data['motor_response'])]

    row = RequestUser(full_name=data['full_name'],
                      age=data['age'],
                      number=int(data['number']),
                      srad=srad,
                      creatinine=data['creatinine'],
                      bilirubin=data['bilirubin'],
                      platelets=data['platelets'],
                      pao2_fio2=data['pao2_fio2'],
                      eye_response=eye_response,
                      verbal_response=verbal_response,
                      motor_response=motor_response,
                      )
    row.save()
    return None
