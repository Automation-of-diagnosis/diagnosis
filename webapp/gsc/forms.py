from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

choices_srad = [
    ('0', ''),
    ('1', 'АД среднее <70 мм рт.ст.'),
    ('2', 'Допамин <= 5 или любая доза добутамина'),
    ('3', 'Допамин > 5 или адреналин <= 0,1, или норадреналин <= 0,1'),
    ('4', 'Допамин > 15 или адреналин > 0,1, или норадреналин > 0,1'),
]

choices_eye_response = [
    ('0', ''),
    ('4', 'Спонтанное'),
    ('3', 'В ответ на словесный приказ'),
    ('2', 'В ответ на болевое раздражение'),
    ('1', 'Отсутствует'),
]

choices_verbal_response = [
    ('0', ''),
    ('5', 'Быстрые ответы'),
    ('4', 'Спутанная речь'),
    ('3', 'Бессмысленные слова'),
    ('2', 'Нечленораздельные звуки'),
    ('1', 'Отсутствует'),
]

choices_motor_response = [
    ('0', ''),
    ('6', 'Целенаправленная в ответ на инструкцию'),
    ('5', 'Локализация болевого раздражителя'),
    ('4', 'Отдергивание в ответ на болевое раздражение'),
    ('3', 'Сгибание в ответ на болевое раздражение'),
    ('2', 'Разгибание в ответ на болевое раздражение'),
    ('1', 'Отсутствует'),
]


class LoginForm(FlaskForm):
    full_name = StringField('Ф.И.О.', render_kw={"class": "form-control"})
    age = IntegerField('Возраст',  render_kw={"class": "form-control"})
    number = IntegerField('№ истории болезни', validators=[DataRequired()], render_kw={"class": "form-control"})
    srad = SelectField('срАД (мм рт.ст.)', choices=choices_srad)
    creatinine = IntegerField('Креатинин (ммоль/л)',  render_kw={"class": "form-control"})
    platelets = IntegerField('Тромбоциты (10*9/л)',  render_kw={"class": "form-control"})
    bilirubin = IntegerField('Билирубин (ммоль/л)', render_kw={"class": "form-control"})
    pao2_fio2 = IntegerField('PaO2/FiO2 (мм рт.ст.)',  render_kw={"class": "form-control"})
    eye_response = SelectField('Открывание глаз', choices=choices_eye_response)
    verbal_response = SelectField('Словесный ответ', choices=choices_verbal_response)
    motor_response = SelectField('Двигательная реакция', choices=choices_motor_response)
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class AddDataForm(FlaskForm):
    full_name = StringField('Ф.И.О.', render_kw={"class": "form-control"})
    age = IntegerField('Возраст', render_kw={"class": "form-control"})
    srad = SelectField('срАД (мм рт.ст.)', choices=choices_srad)
    creatinine = IntegerField('Креатинин (ммоль/л)', render_kw={"class": "form-control"})
    platelets = IntegerField('Тромбоциты (10*9/л)', render_kw={"class": "form-control"})
    bilirubin = IntegerField('Билирубин (ммоль/л)', render_kw={"class": "form-control"})
    pao2_fio2 = IntegerField('PaO2/FiO2 (мм рт.ст.)', render_kw={"class": "form-control"})
    eye_response = SelectField('Открывание глаз', choices=choices_eye_response)
    verbal_response = SelectField('Словесный ответ', choices=choices_verbal_response)
    motor_response = SelectField('Двигательная реакция', choices=choices_motor_response)
    add = SubmitField('Добавить данные', render_kw={"class": "btn btn-primary"})
